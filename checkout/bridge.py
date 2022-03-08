from .models import ZarrinPayTransaction

class Bridge():
    def start_transaction(self, order_id, basket, total_incl_tax):
        transaction = ZarrinPayTransaction.objects.create(
            order_id = order_id ,
            basket = basket , 
            total_incl_tax = total_incl_tax ,
        )
        return transaction.id

    def get_transaction_from_id_returned_by_zarrinpal_request_query(self, id):
        transaction = ZarrinPayTransaction.objects.get(id=id)
        order_id = transaction.order_id
        basket = transaction.basket
        total_incl_tax = transaction.total_incl_tax
        return (order_id, basket, total_incl_tax, total_incl_tax)
    
    def change_transaction_type_after_pay(self, id, status) :
        transaction = ZarrinPayTransaction.objects.get(id=id)
        transaction.pay_type = status
        transaction.save()
    