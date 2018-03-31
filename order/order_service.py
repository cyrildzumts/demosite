import datetime
from django.db import connection

from order import models

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