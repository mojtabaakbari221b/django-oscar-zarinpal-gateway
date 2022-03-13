from .models import ZarrinPayTransaction

class Bridge():
    """
    A bridge between oscar's and zarrinpal's objects
    """

    def start_transaction(self, order_id, basket, total_excl_tax, shipping_address):
        """
        creates a new transaction when redirecting to gateway
        """

        shipping_address.save()
        pay_transaction = ZarrinPayTransaction.objects.create(
            order_id = order_id ,
            basket = basket , 
            total_excl_tax = total_excl_tax ,
            shipping_address = shipping_address ,
        )
        return pay_transaction.id
    
    def get_shipping_address(self, pay_transaction):
        """
        returnes shipping_address from pay_transaction
        """
        return pay_transaction.shipping_address

    def get_transaction_from_id_returned_by_zarrinpal_request_query(self, id):
        """
        returnes ZarrinPayTransaction instance from id,
        this id returned by zarrinpal gateway
        """
        return ZarrinPayTransaction.objects.get(id=id)
    
    def change_transaction_type_after_pay(self, pay_transaction, status) :
        """
        changes ZarrinPayTransaction instance pay_type,
        PANDING --> redirect to gateway but not came back yet,
        DEFERRED --> unsucessful payment
        IN_TROUBLE_BUT_PAID --> this is a bad situation, transaction payed in zarrinpal, 
            but something make problem in submit . you can check this situtation 
            periodic in django admin .
        AUTHENTICATE --> sucessful payment and submit
        """
        pay_transaction.pay_type = status
        pay_transaction.save()
    