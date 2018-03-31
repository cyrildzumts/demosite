import datetime
from django.db import connection

from wishlist import models


class WishlistService():

    @staticmethod
    def contains_item(wishlist_id, product_id):
        flag = False
        result = None
        query = "SELECT  1 from  wishlistitems_wishlists as content \
            LEFT JOIN wishlists as wl on wl.id =content.wishlist_id \
			LEFT JOIN wishlistitems as wi on wi.id=content.wishlistitem_id \
            WHERE wl.id=%s and wi.product_id =%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [wishlist_id, product_id])
            result = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Wishlistservice : contains_item() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            flag = 1 in result
        return flag
    

    @staticmethod
    def items_count(wishlist_id):
        count = 0
        result = None
        query = "SELECT COUNT(content.id) as counter from  wishlistitems_wishlists as content \
            WHERE content.wishlist_id=%s"
        
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [wishlist_id])
            result = cursor.fetchall()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Wishlistservice : items_count() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        
        if result and len(result):
            count = result[0]

        return count