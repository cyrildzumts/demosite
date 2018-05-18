import datetime
from django.db import connection
from cart.cart_service import CartService
from order.forms import CheckoutForm
from order import models
from order import payment, payment_providers

class OrderService():
    @staticmethod
    def get_total(order_id):
        total = 0
        result = None
        query = "SELECT  SUM(content.price *content.quantity) as SUM_TOTAL from  order_orderitem as content \
            LEFT JOIN order_order as orders on content.order_id=orders.id \
            WHERE content.order_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [order_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Orderservice : get_total() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            total = result[0]
        return total
    

    @staticmethod
    def create_order(request):
        order = models.Order()
        checkout_form = CheckoutForm(request.POST, instance=order)
        if checkout_form.is_valid():

            order = checkout_form.save(commit=False)
            order.ip_address = request.META.get('REMOTE_ADDR')
            order.user = request.user
            order.status = models.Order.SUBMITTED
            order.generate_order_refNum()
            order.save()
        # if order save succeeded
            if order.pk:
                cart_items = CartService.get_user_cart(request).get_items()
                for ci in cart_items:
                    # create order item for each cart item
                    oi = models.OrderItem()
                    oi.order = order
                    oi.quantity = ci.quantity
                    oi.price = ci.price()  # using @property
                    oi.product = ci.product
                    oi.save()

        return order


    @staticmethod
    def process_order(request):
        order = OrderService.create_order(request)
        charged = OrderService.charge_order(order)
        return charged

    
    @staticmethod
    def get_user_cart(request):
        pass
    
    @staticmethod
    def charge_order(order):
        provider = payment_providers.AirtelMoneyProviderMock()
        pay = payment.SMSPayment(provider)
        return pay.process_payment(order)