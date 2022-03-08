from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.checkout.mixins import OrderPlacementMixin
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponse
from .gateway import  do_pay, check_call_back
from oscar.apps.payment import models
from oscar.apps.payment.exceptions import (
    UserCancelled,
    InsufficientPaymentSources,
)
import logging
logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(CorePaymentDetailsView):
    def handle_payment(self, order_number, order_total, **payment_kwargs):
        return do_pay(self.request , order_number , order_total)
        

class CheckZarrinPalCallBack(View, OrderPlacementMixin):
    def get(self, request):
        try :
            if check_call_back(request) :
                amount = request.GET.get('amount')
                source_type, is_created = models.SourceType.objects.get_or_create(
                name='ZarrinPal')

                source = source_type.sources.model(
                    source_type=source_type,
                    amount_allocated=amount,
                    currency='IRR',
                )

                self.add_payment_source(source)
                self.add_payment_event('Authorised', amount)
              
        except InsufficientPaymentSources as e :
            # Exception for when a user attempts to checkout without specifying enough
            # payment sources to cover the entire order total.
            # Eg. When selecting an allocation off a giftcard but not specifying a
            # bankcard to take the remainder from. 
            pass
        
        except UserCancelled as e :
            # During many payment flows,
            # the user is able to cancel the process. This should often be treated
            # differently from a payment error, e.g. it might not be appropriate to offer
            # to retry the payment.
            pass
        
        except Exception as e :
            # Unhandled exception - hopefully, you will only ever see this in
            # development.
            logger.error("Order #%s: unhandled exception while taking payment (%s)", request.GET.get("order_number"), e)
            logger.exception(e)
        
        return HttpResponse(f'result {request.GET.get("order_number")}')    

