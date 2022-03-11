from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.checkout.mixins import Basket, OrderPlacementMixin
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _
from oscar.apps.checkout import signals
from .bridge import Bridge
from .gateway import  do_pay, check_call_back
from oscar.apps.payment import models
from django.http import HttpResponseRedirect
from oscar.apps.order.exceptions import (
    UnableToPlaceOrder,
)
from oscar.apps.payment.exceptions import (
    GatewayError,
    UserCancelled,
    InsufficientPaymentSources,
    RedirectRequired,
)
from .models import ZarrinPayTransaction
import logging
logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(CorePaymentDetailsView):
    def submit(self, user, basket, shipping_address, shipping_method,  # noqa (too complex (10))
               shipping_charge, billing_address, order_total,
               payment_kwargs=None, order_kwargs=None, surcharges=None):
        """
        Submit a basket for order placement.

        The process runs as follows:

         * Generate an order number
         * Freeze the basket so it cannot be modified any more (important when
           redirecting the user to another site for payment as it prevents the
           basket being manipulated during the payment process).
         * Attempt to take payment for the order
           - If payment is successful, place the order
           - If a redirect is required (e.g. PayPal, 3D Secure), redirect
           - If payment is unsuccessful, show an appropriate error message

        :basket: The basket to submit.
        :payment_kwargs: Additional kwargs to pass to the handle_payment
                         method. It normally makes sense to pass form
                         instances (rather than model instances) so that the
                         forms can be re-rendered correctly if payment fails.
        :order_kwargs: Additional kwargs to pass to the place_order method
        """
        if payment_kwargs is None:
            payment_kwargs = {}
        if order_kwargs is None:
            order_kwargs = {}

        # Taxes must be known at this point
        assert basket.is_tax_known, (
            "Basket tax must be set before a user can place an order")
        assert shipping_charge.is_tax_known, (
            "Shipping charge tax must be set before a user can place an order")

        # We generate the order number first as this will be used
        # in payment requests (ie before the order model has been
        # created).  We also save it in the session for multi-stage
        # checkouts (e.g. where we redirect to a 3rd party site and place
        # the order on a different request).
        order_number = self.generate_order_number(basket)
        self.checkout_session.set_order_number(order_number)
        logger.info("Order #%s: beginning submission process for basket #%d",
                    order_number, basket.id)

        # Freeze the basket so it cannot be manipulated while the customer is
        # completing payment on a 3rd party site.  Also, store a reference to
        # the basket in the session so that we know which basket to thaw if we
        # get an unsuccessful payment response when redirecting to a 3rd party
        # site.
        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

        # We define a general error message for when an unanticipated payment
        # error occurs.
        error_msg = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")

        signals.pre_payment.send_robust(sender=self, view=self)

        try:
            # shipping_address = self.create_shipping_address(user, shipping_address)
            # print(type(shipping_charge.currency))
            # print(type(order_total))
            # print(order_total)
            # raise GatewayError
            shipping_address.save()
            self.check_currency(order_total.currency)
            self.handle_payment(order_number, basket, order_total, shipping_address, shipping_method,   **payment_kwargs)
        except RedirectRequired as e:
            # Redirect required (eg ZarrinpalPay)
            logger.info("Order #%s: redirecting to %s", order_number, e.url)
            return HttpResponseRedirect(e.url)
        except Exception as e:
            # Unhandled exception - hopefully, you will only ever see this in
            # development...
            logger.exception(
                "Order #%s: unhandled exception while taking payment (%s)",
                order_number, e)
            self.restore_frozen_basket()
            return self.render_preview(
                self.request, error=error_msg, **payment_kwargs)

    def check_currency(self, currency):
        if not currency == 'IRR' :
            raise GatewayError

    def return_total_tax(self, order_total):
        return int(order_total.excl_tax)

    def handle_payment(self, order_number, basket, order_total, shipping_address, shipping_method, **payment_kwargs):
        total_excl_tax = self.return_total_tax(order_total)
        return do_pay(self.request , order_number, basket , total_excl_tax, shipping_address, shipping_method)
    
class CheckZarrinPalCallBack(OrderPlacementMixin, View):
    template_name = 'checkout/call_back_result.html'

    def create_shipping_address(self, user, shipping_address):
        shipping_address = self.bridge.get_shipping_address(self.pay_transaction )
        if user.is_authenticated:
            self.update_address_book(user, shipping_address)
        return shipping_address
    
    def create_context_for_template(self, order_number, status_code, msg=None,) -> dict:
        return {
            "number" : order_number,
            "msg" : msg,
            "status" : status_code,
        }

    def render_tamplate(self ,order_id ,status_code=200):
        context = self.create_context_for_template(order_id, status_code)
        return render(self.request, self.template_name , context=context, status=status_code)
    
    def get(self, request, bridge_id, *args, **kwargs):
        status_code = 200
        try :
            self.bridge = Bridge()
            self.pay_transaction = self.bridge.get_transaction_from_id_returned_by_zarrinpal_request_query(bridge_id)

            if check_call_back(request, self.pay_transaction.total_excl_tax) :
                response =  self.submit_order()
                self.change_transaction_pay_type(status=status_code, pay_transaction=self.pay_transaction)
                return response
              
        except InsufficientPaymentSources as e :
            # Exception for when a user attempts to checkout without specifying enough
            # payment sources to cover the entire order total.
            # Eg. When selecting an allocation off a giftcard but not specifying a
            # bankcard to take the remainder from.
            logger.error("Order #%s: insufficient payment sources the pay (%s)", self.pay_transaction.order_id, e)
            logger.exception(e)
            status_code=402
        
        except UserCancelled as e :
            # During many payment flows,
            # the user is able to cancel the process. This should often be treated
            # differently from a payment error, e.g. it might not be appropriate to offer
            # to retry the payment.
            logger.error("Order #%s: user cancelled the pay (%s)", self.pay_transaction.order_id, e)
            logger.exception(e)
            status_code=410
        
        except (UnableToPlaceOrder, TypeError) as e :
            # It's possible that something will go wrong while trying to
            # actually place an order.  Not a good situation to be in, but needs
            # to be handled gracefully.
            logger.error("Order #%s: unable to place order while taking payment (%s)", self.pay_transaction.order_id, e)
            logger.exception(e)
            status_code = 422
        
        except Exception as e :
            # Unhandled exception - hopefully, you will only ever see this in
            # development.
            logger.error("Order #%s: unhandled exception while taking payment (%s)", self.pay_transaction.order_id, e)
            logger.exception(e)
            status_code=500

        self.change_transaction_pay_type(status=status_code, pay_transaction=self.pay_transaction)
        return self.render_tamplate(order_id=self.pay_transaction.order_id, status_code=status_code)

    def submit_order(self):

        source_type, is_created = models.SourceType.objects.get_or_create(
            name='ZarrinPal'
        )
    
        source = models.Source(
            source_type=source_type,
            currency='IRR',
            amount_allocated=self.pay_transaction.total_excl_tax,
        )

        self.add_payment_source(source)
        self.add_payment_event('Authorised', self.pay_transaction.total_excl_tax)

        # from oscar.apps.basket.abstract_models

        # finalising the order into oscar
        logger.info("Order #%s: payment successful, placing order", self.pay_transaction.order_id)

        from oscar.apps.partner.strategy import Default as DefaultStrategy
        self.pay_transaction.basket.strategy = DefaultStrategy()

        shipping_method = self.bridge.get_shipping_method_from_db(self.pay_transaction)

        from oscar.core.prices import Price
        shipping_charge = Price(
            currency='IRR' ,
            excl_tax= 0 ,
            incl_tax= 0,
            tax= 0,
        )
        order_total = Price(
            currency='IRR' ,
            excl_tax= self.pay_transaction.total_excl_tax ,
            incl_tax= self.pay_transaction.total_excl_tax ,
            tax= 0,
        )
        # from oscar.apps.basket.abstract_models
        
        return self.handle_order_placement(
            order_number=self.pay_transaction.order_id,
            basket=self.pay_transaction.basket,
            order_total=order_total, 
            user=self.request.user,
            shipping_address = self.pay_transaction.shipping_address,
            shipping_method = shipping_method,
            shipping_charge = shipping_charge,
            billing_address=None,
        )

    def change_transaction_pay_type(self, status, pay_transaction):
        if status == 200 :
            pay_status = ZarrinPayTransaction.AUTHENTICATE
        elif status == 422 :
            pay_status = ZarrinPayTransaction.IN_TROUBLE_BUT_PAID
        else :
            self.restore_frozen_basket()
            pay_status = ZarrinPayTransaction.DEFERRED
        self.bridge.change_transaction_type_after_pay(self.pay_transaction ,pay_status)