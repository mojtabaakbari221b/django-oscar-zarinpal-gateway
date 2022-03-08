from django.conf import settings
from django.contrib.sites.models import Site

site = Site.objects.get_current()
DOMAIN = site.domain

DEFAULT_ZARINPAL_CONFIGURATION = {
    'MECHANT_ID' : 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
    'WEBSERVICE' : 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl',
    'USE_SANDBOX' : True,
    'STARTPAY_URL': 'https://sandbox.zarinpal.com/pg/StartPay/',
}

ZARINPAL_CONFIGURATION = getattr(settings , "ZARINPAL_CONFIGURATION" , DEFAULT_ZARINPAL_CONFIGURATION)

MMERCHANT_ID = ZARINPAL_CONFIGURATION.get("MECHANT_ID")
WEBSERVICE = ZARINPAL_CONFIGURATION.get("WEBSERVICE")
STARTPAY_URL = ZARINPAL_CONFIGURATION.get("STARTPAY_URL")



