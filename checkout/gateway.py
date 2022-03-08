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

def do_pay(request, order_number , order_total):
    # raise GatewayError
    client = Client(WEBSERVICE)
    # if order_total.currency != 'IRR' : # check currency is iranian RIAL
    #     raise InvalidGatewayRequestError("while you use zarinpal-gateway, you shoud use IRR currency")
    redirect_url = DOMAIN + reverse('checkout:zarinpal-callback') + f'?order_number={order_number}&amount={order_total.incl_tax}'
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

def check_call_back(request):
    if request.GET.get('Status') == 'OK':
        client = Client(WEBSERVICE)

        amount = request.GET.get('amount')
        
        result = client.service.PaymentVerification(
            MMERCHANT_ID,
            request.GET.get('Authority'),
            amount,
        )

        if result.Status == 100 or result.Status == 101 :
            return True
        else:
            raise InsufficientPaymentSources
    else:
        raise UserCancelled

