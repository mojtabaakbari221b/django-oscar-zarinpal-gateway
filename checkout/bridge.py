from .models import ZarrinPayTransaction

class Bridge():
    def start_transaction(self, order_id, basket, total_excl_tax):
        transaction = ZarrinPayTransaction.objects.create(
            order_id = order_id ,
            basket = basket , 
            total_excl_tax = total_excl_tax ,
        )
        return transaction.id

    def get_transaction_from_id_returned_by_zarrinpal_request_query(self, id):
        return ZarrinPayTransaction.objects.get(id=id)
    
    def change_transaction_type_after_pay(self, id, status) :
        transaction = ZarrinPayTransaction.objects.get(id=id)
        transaction.pay_type = status
        transaction.save()
    