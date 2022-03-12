====================
django-oscar-zarrinpal-gateway
====================

Payment gateway integration for `Zarinpal Payments <https://www.zarinpal.com>`_ in django-oscar_.
Zarinpal Payments is a large payment gateway based in The I.R. Iran .

.. _django-oscar: https://github.com/django-oscar/django-oscar


Installation
============

Install via pip:

.. code-block:: bash

    pip install django-oscar-zarrinpal-gateway


Configuration
-------------

Configure the application in settings.py:

`ZARRIN_USE_SANDBOX` (optional)
    app use sandbox for payment by default, for disable set this to False.

`ZARRIN_MERCHANT_ID`
    zarrin pal merchand id .
    If you do not enter a valid value, you will encounter the problem of non-approval .
    Also, if you do not use the sandbox, you will receive an error if you do not enter this value

`ZARRIN_ERROR_MSG_UNSECESSFUL_PAGE` (optional)
    this message showed when unexpected error happen before redirect to zarrinpal gateway.

The following values ​​are for after payment messages :

`ZARRIN_402_PAYMENT_MSG` (optional)
    unsucessfull payment in zarrin pal message .

`ZARRIN_410_PAYMENT_MSG` (optional)
    process cancelled in zarrin pal message .

`ZARRIN_422_PAYMENT_MSG` (optional)
    This message is displayed when payment is made correctly but the user's shopping cart is not approved .
    It is one of the error modes that Django Oscar raises .
    You can read Django Oscar's document for more information .

`ZARRIN_500_PAYMENT_MSG` (optional)
    Do not worry . In this case, the user's shopping cart becomes unpaid. Django Oscar used an interesting phrase in his document : hopefully, you will only ever see this in
    development...


in ``settings.py``:

comment 'oscar.apps.checkout.apps.CheckoutConfig',
and add 'django_oscar_zarinpal_gateway.checkout.apps.ZarrinCheckoutConfig'

.. code-block:: python

    INSTALLED_APPS = [
        ...,

        # 'oscar.apps.checkout.apps.CheckoutConfig',
        django_oscar_zarinpal_gateway.checkout.apps.ZarrinCheckoutConfig'
        ...,
    ]

add OSCAR_PAYMENT_METHODS in ``settings.py``:

.. code-block:: python

    OSCAR_PAYMENT_METHODS = (
        ('django_oscar_zarinpal_gateway', ('Django Zarrin Pal')),
    )

add 'django_oscar_zarinpal_gateway.checkout' in TEMPLATES['DIRS']

.. code-block:: python

    TEMPLATES = [
        ... ,
        'DIRS': [
            ...,
            'django_oscar_zarinpal_gateway.checkout',
        ],
        ... ,
    ]

run following command :

.. code-block:: python

    python manage.py makemigrations checkout
    python manage.py migrate

important points
-------------

* To use the package, your basket must have its own currency set to IRR.
* if all the activity of your store is related to Iran, you can set the variable OSCAR_DEFAULT_CURRENCY to IRR, You can read Django Oscar's document for more information .


Link
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you find a bug or have a question, you can contact me via the link below `mojtaba.akbari.221B@gmail.com`_.

.. _`mojtaba.akbari.221B@gmail.com`: mailto:mojtaba.akbari.221B@gmail.com