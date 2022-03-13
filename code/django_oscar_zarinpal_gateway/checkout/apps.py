import oscar.apps.checkout.apps as apps
from django.urls import path

class ZarrinCheckoutConfig(apps.CheckoutConfig):
    name = 'django_oscar_zarinpal_gateway.checkout'
    def ready(self):
        super().ready()
        from .views import CheckZarrinPalCallBack
        self.zarinpal_callback = CheckZarrinPalCallBack

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('callback/<int:bridge_id>/', self.zarinpal_callback.as_view(), name='zarinpal-callback'),
        ]
        return self.post_process_urls(urls)