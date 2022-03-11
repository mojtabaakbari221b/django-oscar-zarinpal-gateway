from suds.client import Client
from oscar.apps.payment.exceptions import (
    GatewayError,
    RedirectRequired,
    UserCancelled,
    InsufficientPaymentSources,
)
from django.urls import reverse
from django_oscar_zarinpal_gateway.settings import (
    WEBSERVICE,
    MMERCHANT_ID,
    STARTPAY_URL,
    DOMAIN,
)
from .bridge import Bridge


def do_pay(request, order_id, basket , total_excl_tax, shipping_address, shipping_method):
    client = Client(WEBSERVICE)
    
    bridge = Bridge()
    transaction_id = bridge.start_transaction(order_id, basket, total_excl_tax, shipping_address, shipping_method)
    redirect_url = DOMAIN + reverse('checkout:zarinpal-callback', args=(transaction_id,))
    result = client.service.PaymentRequest(
        MMERCHANT_ID,
        total_excl_tax,
        f"order number : {order_id}",
        request.user.email,
        None,
        redirect_url,
    )
    if result.Status == 100:
        url = STARTPAY_URL + result.Authority
        raise RedirectRequired(url=url)
    else:
        raise GatewayError

def check_call_back(request, total_incl_tax):
    if request.GET.get('Status') == 'OK':
        client = Client(WEBSERVICE)
        
        result = client.service.PaymentVerification(
            MMERCHANT_ID,
            request.GET.get('Authority'),
            total_incl_tax,
        )
        if result.Status == 100 or result.Status == 101 :
            return True
        else:
            raise InsufficientPaymentSources
    else:
        raise UserCancelled

