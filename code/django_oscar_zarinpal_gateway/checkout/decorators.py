from django.urls import resolve, reverse
from django.shortcuts import redirect

def redirect_payment_detail_to_payment_method(func):
    payment_detail_route = 'checkout:payment-details'
    payment_method_route = 'checkout:payment-method'

    def inner(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).route
        payment_detail_url = resolve(reverse(payment_detail_route)).route
        if current_url == payment_detail_url :
            return redirect(payment_method_route)
        else :
            return func(self, request, *args, **kwargs)
        
    return inner