from suds.client import Client
from oscar.apps.payment.exceptions import (
    GatewayError,
    RedirectRequired,
)
from django.urls import reverse
from django_oscar_zarinpal_gateway.settings import (
    WEBSERVICE,
    MMERCHANT_ID,
    STARTPAY_URL,
    DOMAIN,
)

def do_pay(request, order_number , order_total):
    client = Client(WEBSERVICE)
    # if order_total.currency != 'IRR' : # check currency is iranian RIAL
    #     raise InvalidGatewayRequestError("while you use zarinpal-gateway, you shoud use IRR currency")
    redirect_url = DOMAIN + reverse('checkout:zarinpal-callback') + f'?order_number={order_number}'
    result = client.service.PaymentRequest(
        MMERCHANT_ID,
        order_total.excl_tax * 30000,
        f"order number : {order_number}",
        request.user.email,
        None,
        redirect_url,
    )
    if result.Status == 100:
        url = STARTPAY_URL + result.Authority
        raise RedirectRequired(url=url)
    else:
        raise GatewayError