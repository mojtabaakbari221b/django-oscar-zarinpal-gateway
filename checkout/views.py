from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.payment.exceptions import PaymentError
from suds.client import Client
from django_oscar_zarinpal_gateway.settings import (
    ZARINPAL_WEBSERVICE,
    MMERCHANT_ID,
    DESCRIPTION,
)
from django.views import View
from django.http import HttpResponse

class PaymentDetailsView(CorePaymentDetailsView):
    def handle_payment(self, order_number, order_total, **payment_kwargs):
        client = Client(ZARINPAL_WEBSERVICE)
        result = client.service.PaymentRequest(MMERCHANT_ID,
                                            1000,
                                            DESCRIPTION,
                                            self.request.user.email,
                                            None,
                                            user_data_dictionary.get("call_back_url"))
        print(order_number)
        print(order_total)
        raise PaymentError("hello")

class CheckZarrinPalCallBack(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')    
