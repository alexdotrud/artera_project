from django.contrib import admin
from .models import Order, OrderItem

class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    # calculated/auto fields should be read-only
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
    )

    # field layout in the admin detail page
    fields = (
        'order_number',
        'date',

        'full_name',
        'email',
        'phone_number',

        'country',
        'postcode',
        'town_or_city',
        'street_address1',
        'street_address2',
        'county',

        'delivery_cost',
        'order_total',
        'grand_total',
    )

    # columns in the list view
    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'delivery_cost',
        'grand_total',
    )

    ordering = ('-date',)
