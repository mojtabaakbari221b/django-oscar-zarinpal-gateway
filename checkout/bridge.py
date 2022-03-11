from .models import ZarrinPayTransaction

class Bridge():
    def start_transaction(self, order_id, basket, total_excl_tax, shipping_address, shipping_method):
        shipping_method_module , shipping_method_class = self.shipping_method_module_and_class_name_from_instance(shipping_method)
        pay_transaction = ZarrinPayTransaction.objects.create(
            order_id = order_id ,
            basket = basket , 
            total_excl_tax = total_excl_tax ,
            shipping_address = shipping_address ,
            shipping_method_module = shipping_method_module ,
            shipping_method_class = shipping_method_class ,
        )
        return pay_transaction.id
    
    def get_shipping_address(self, pay_transaction):
        return pay_transaction.shipping_address
    
    def get_shipping_method_from_db(self, pay_transaction):
        imported_class = self.__import(f"{pay_transaction.shipping_method_module}.{pay_transaction.shipping_method_class}")
        return imported_class()

    def __import(self, class_name):
        components = class_name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
    def shipping_method_module_and_class_name_from_instance(self, class_instance):
        return (
            class_instance.__class__.__module__ ,
            class_instance.__class__.__name__ ,
        ) 

    def get_transaction_from_id_returned_by_zarrinpal_request_query(self, id):
        return ZarrinPayTransaction.objects.get(id=id)
    
    def change_transaction_type_after_pay(self, pay_transaction, status) :
        pay_transaction.pay_type = status
        pay_transaction.save()
    