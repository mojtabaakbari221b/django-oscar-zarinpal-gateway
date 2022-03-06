from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.payment.exceptions import PaymentError

class PaymentDetailsView(CorePaymentDetailsView):
    def handle_payment(order_number, order_total, **payment_kwargs):
        raise PaymentError("hello")

    
