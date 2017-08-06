from django.contrib import admin
from order.models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    exclude = ['transaction_id', 'ip_address', 'shipping_zip']
    fields = ['paid_status', 'paid_at', 'user', 'ref_num']
    empty_value_display = 'unknown'
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
