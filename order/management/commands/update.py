from order.models import Order, OrderItem
from catalog.models import Product
from datetime import datetime


class StoreUpdater(object):
    today = datetime.now()
    days_max = 7
    def __init__(self):
        # contains a Orders to be deleted
        self.to_delete_orders = []
        # contains QuerySet of OrderItems
        self.queryset_orderItem_to_update = []
        # contains list of unpaid orders
        self.unpaid_orders = []
        # contains OrderItems
        self.ordered_item_set = []
    def isDayLimitExceeded(self, item):
        flag = False
        if type(item) == Order:
            flag = (StoreUpdater.today.date() - item.date.date()).days > StoreUpdater.days_max
        return flag

    def fetchUnpaid(self):
        self.unpaid_orders = Order.objects.filter(paid_status=False)

    def fetchToDelete(self):
        unpaid_orders = Order.objects.filter(paid_status=False)
        self.to_delete_orders = [item for item in unpaid_orders if self.isDayLimitExceeded(item)]
        for order in self.to_delete_orders:
            self.queryset_orderItem_to_update.append(order.orderitem_set.all())

    def getUpdatedProductSet(self):
        print("Updating Products in the Store ...")
        for entryset in self.queryset_orderItem_to_update:
            for orderitem in entryset:
                orderitem.product.quantity +=  orderitem.quantity
                orderitem.product.save()
        print("Products updated ...")

    def deleteAllUnpaidOrders(self):
        print("Deleting all unpaid orders...")
        self.fetchUnpaid()
        queryset = []
        for order in self.unpaid_orders:
            queryset.append(order.orderitem_set.all())
        print("Updating Products in the Store ...")
        for entryset in queryset:
            for orderitem in entryset:
                orderitem.product.quantity +=  orderitem.quantity
                orderitem.product.save()
        print("Products updated ...")
        self.unpaid_orders.delete()
        print("Deleting all unpaid orders done ! ...")

    def deleteOrderedItems(self):
        print("Deleting unpaid Orders ...")
        for order in self.to_delete_orders:
            order.delete()
        print("Deleting unpaid Orders done !...")

    def updadeStore(self):
        print("Updating the Store ...")
        self.fetchToDelete()
        if(self.to_delete_orders):
            print(self.to_delete_orders)
            self.getUpdatedProductSet()
            self.deleteOrderedItems()
        else:
            print("Nothing to be deleted")
        print("Updating the Store done ...")

def update_store():
    pass