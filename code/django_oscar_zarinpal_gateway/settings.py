from oscar import defaults
import logging
if not getattr(defaults , "OSCAR_DEFAULT_CURRENCY" , None) == 'IRR' :
    logging.error("\nwhen you use django_zarrin_pal for gateway backend, recommended set OSCAR_DEFAULT_CURRENCY to IRR, \
        or be careful, your basket currency should be IRR")

from django.contrib.sites.models import Site
DOMAIN = Site.objects.get_current().domain


from django.conf import settings
from django.utils.translation import gettext as _

if getattr(settings, 'ZARRIN_USE_SANDBOX', True) :
    MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    WEBSERVICE = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'
    STARTPAY_URL = 'https://sandbox.zarinpal.com/pg/StartPay/'
else:
    MMERCHANT_ID = getattr(settings, 'ZARRIN_MERCHANT_ID')
    WEBSERVICE = 'https://zarinpal.com/pg/services/WebGate/wsdl'
    STARTPAY_URL = 'https://zarinpal.com/pg/StartPay/'

# define a general error message for when an unanticipated payment
# error occurs.
DEFAULT_ERROR_MSG_UNSECESSFUL_PAGE = _("A problem occurred while processing payment for this "
                      "order - no payment has been taken.  Please "
                      "contact customer services if this problem persists")
ERROR_MSG_UNSECESSFUL_PAGE = getattr(settings, 'ZARRIN_ERROR_MSG_UNSECESSFUL_PAGE', DEFAULT_ERROR_MSG_UNSECESSFUL_PAGE)

# InsufficientPaymentSources
DEFAULT_402_PAYMENT_MSG = 'unsucessfull payment in zarrin pal .'
ZARRIN_402_PAYMENT_MSG = getattr(settings, 'ZARRIN_402_PAYMENT_MSG', DEFAULT_402_PAYMENT_MSG)

# UserCancelled
DEFAULT_410_PAYMENT_MSG = 'process cancelled in zarrin pal .'
ZARRIN_410_PAYMENT_MSG = getattr(settings, 'ZARRIN_410_PAYMENT_MSG', DEFAULT_410_PAYMENT_MSG)

# UnableToPlaceOrder
ZARRIN_422_PAYMENT_MSG = 'your process was well in zarrin pal .\
            but something went wrong in our site, \
            Help us improve your experience by sending an error report .'
ZARRIN_422_PAYMENT_MSG = getattr(settings, 'ZARRIN_420_PAYMENT_MSG', ZARRIN_422_PAYMENT_MSG)

# UnexpectedException
DEFAULT_500_PAYMENT_MSG = 'Oops! Something went wrong !\
                Help us improve your experience by sending an error report . '
ZARRIN_500_PAYMENT_MSG = getattr(settings, 'ZARRIN_500_PAYMENT_MSG', DEFAULT_500_PAYMENT_MSG)

DEFAULT_ZARRIN_INFO_TEXT = 'Django Zarin Pal Gateway'
ZARRIN_INFO_TEXT = getattr(settings, 'ZARRIN_INFO_TEXT', DEFAULT_ZARRIN_INFO_TEXT)
