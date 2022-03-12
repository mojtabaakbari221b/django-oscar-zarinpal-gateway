from oscar.apps.order.models import ShippingAddress
from oscar.apps.checkout.models import *
from django.db import models
from oscar.apps.basket.models import Basket

class ZarrinPayTransaction(models.Model):
    """
    Main zarinpal transaction model.
    """

    PANDING = 'PAYMENT'
    DEFERRED = 'DEFERRED'
    AUTHENTICATE = 'AUTHENTICATE'
    IN_TROUBLE_BUT_PAID = 'IN_TROUBLE_BUT_PAID'
    PAY_TYPE = (
        (PANDING, 'PANDING'),
        (DEFERRED, 'DEFERRED'),
        (AUTHENTICATE, 'AUTHENTICATE'),
        (IN_TROUBLE_BUT_PAID, 'IN_TROUBLE_BUT_PAID'),
    )
    
    order_id = models.PositiveBigIntegerField()
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
    )
    total_excl_tax = models.PositiveBigIntegerField()
    pay_type = models.CharField(
        choices=PAY_TYPE,
        default=PANDING,
        max_length=20,
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

