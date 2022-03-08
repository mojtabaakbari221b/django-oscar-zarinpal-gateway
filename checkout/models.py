from oscar.apps.checkout.models import *
from django.db import models
from oscar.apps.basket.models import Basket

class ZarrinPayTransaction(models.Model):
    PAYMENT = 'PAYMENT'
    DEFERRED = 'DEFERRED'
    AUTHENTICATE = 'AUTHENTICATE'
    PAY_TYPE = (
        (PAYMENT, 'PAYMENT'),
        (DEFERRED, 'DEFERRED'),
        (AUTHENTICATE, 'AUTHENTICATE'),
    )
    
    order_id = models.PositiveBigIntegerField()
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    total_incl_tax = models.PositiveBigIntegerField()
    pay_type = models.CharField(choices=PAY_TYPE, default=PAYMENT, max_length=15)

