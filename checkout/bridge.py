from .models import ZarrinPayTransaction

class Bridge():
    def start_transaction(self, order_id, basket, total_excl_tax, shipping_address):
        shipping_address.save()
        pay_transaction = ZarrinPayTransaction.objects.create(
            order_id = order_id ,
            basket = basket , 
            total_excl_tax = total_excl_tax ,
            shipping_address = shipping_address ,
        )
        return pay_transaction.id
    
    def get_shipping_address(self, pay_transaction):
        return pay_transaction.shipping_address

    def get_transaction_from_id_returned_by_zarrinpal_request_query(self, id):
        return ZarrinPayTransaction.objects.get(id=id)
    
    def change_transaction_type_after_pay(self, pay_transaction, status) :
        pay_transaction.pay_type = status
        pay_transaction.save()
    