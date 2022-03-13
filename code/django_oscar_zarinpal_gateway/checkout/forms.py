from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class PaymentMethodForm(forms.Form):
    """
    Extra form for the custom payment method.
    """
    payment_method = forms.ChoiceField(
        label=_("Select a payment method"),
        choices=settings.OSCAR_PAYMENT_METHODS,
        widget=forms.RadioSelect()
    )


def get_payment_method_display(payment_method):
    return dict(settings.OSCAR_PAYMENT_METHODS).get(payment_method)