from django.contrib import admin
from .models import ZarrinPayTransaction

class ZarrinPayTransactionModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'order_id',
        'basket',
        'pay_type',
        'total_excl_tax',
    ]

admin.site.register(ZarrinPayTransaction, ZarrinPayTransactionModelAdmin)

