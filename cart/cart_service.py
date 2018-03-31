import datetime
from django.db import connection

from cart import models

class CartService():

    @staticmethod
    def get_subtotal(cart_id):
        total = 0
        result = None
        query = "SELECT  SUM(p.price *content.quantity) as SUM_TOTAL from  cart_items as content \
            LEFT JOIN carts as cart on content.cart_id=cart.id \
            LEFT JOIN Product as p on p.id = content.product_id \
            WHERE content.cart_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : get_subtotal() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            total = result[0]
        return total


    @staticmethod
    def items_count(cart_id):
        count = 0
        result = None
        query = "SELECT SUM(content.quantity) as counter from  cart_items as content \
            WHERE content.cart_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : items_count() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            count = result[0]

        return count

    @staticmethod
    def contains_item(cart_id, product_id):
        flag = False
        result = None
        query = "SELECT  1 from  cart_items as content \
            LEFT JOIN carts as cart on cart.id =content.cart_id \
            WHERE content.cart_id=%s and content.product_id = %s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [cart_id, product_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Cartservice : contains_item() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            flag = 1 in result
        return flag



def cart_test():
    cart = models.Cart.objects.get(id=32)
    total_1 = cart.subtotal()
    total_2 = CartService.get_subtotal(cart.id)

    counter_1 = cart.items_count()
    counter_2 = CartService.items_count(cart.id)

    flag_1 = cart.contain_item(1)
    flag_2 = CartService.contains_item(cart.id, 1)
    print("total_1 : {0} \n \
           total_2 : {1} \n \
           counter_1 : {2} \n \
           counter_2 : {3}".format(total_1, total_2, counter_1, counter_2))

    print("Flag_1 : {0} \n \
           Flag_2 : {1}".format(flag_1, flag_2))