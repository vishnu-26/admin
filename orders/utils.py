from .models import Order,OrderItem


def get_order_detail(pk):
    order = list(Order.objects.filter(id= pk).values())[0]
    
    order_items = list(OrderItem.objects.filter(id= pk).values())
    order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
    order['order_items'] = order_items
    return order


def get_orders_details(_orders):
    orders = list(_orders.values())

    for order in orders:
        order_items = list(OrderItem.objects.filter(order= order['id']).values())
        order['total_price'] = sum((order_item['price']*order_item['quantity']) for order_item in order_items)
        order['order_items'] = order_items

    return orders
