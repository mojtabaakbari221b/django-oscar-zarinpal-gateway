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
    ZARRIN_INFO_TEXT,
)
from .bridge import Bridge


def do_pay(request, order_id, basket , total_excl_tax, shipping_address):
    """
    Handle the communication with zarrinpal server
    connect to server with MMERCHANT_ID,
    if MMERCHANT_ID is valid,
    redirect users to zarrinpal server.
    """

    client = Client(WEBSERVICE)

    if callable(ZARRIN_INFO_TEXT) :
        info = str(ZARRIN_INFO_TEXT(request, order_id))
    else :
        info = str(ZARRIN_INFO_TEXT)
    
    bridge = Bridge()
    transaction_id = bridge.start_transaction(order_id, basket, total_excl_tax, shipping_address)
    redirect_url = DOMAIN + reverse('checkout:zarinpal-callback', args=(transaction_id,))
    result = client.service.PaymentRequest(
        MMERCHANT_ID,
        total_excl_tax,
        info,
        request.user.email,
        None,
        redirect_url,
    )
    if result.Status == 100:
        url = STARTPAY_URL + result.Authority
        raise RedirectRequired(url=url)
    else:
        raise GatewayError

def check_call_back(request, total_excl_tax):
    """
    Handle the communication back with zarrinpal server
    connect to server with Authority that returned by zarrinpal server,
    returns true mean everything is OK if authority and total_excl_tax is valid.
    """

    if request.GET.get('Status') == 'OK':
        client = Client(WEBSERVICE)
        
        result = client.service.PaymentVerification(
            MMERCHANT_ID,
            request.GET.get('Authority'),
            total_excl_tax,
        )
        if result.Status == 100 or result.Status == 101 :
            return True
        else:
            raise InsufficientPaymentSources
    else:
        raise UserCancelled

