from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from django.views import View
from django.http import HttpResponse
from django.http import HttpResponse
from .gateway import  do_pay
import logging
logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(CorePaymentDetailsView):
    def handle_payment(self, order_number, order_total, **payment_kwargs):
        return do_pay(self.request , order_number , order_total)

class CheckZarrinPalCallBack(View):
    def get(self, request):
        return HttpResponse(f'result {request.GET["order_number"]}')    

