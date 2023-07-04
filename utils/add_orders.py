from WmVoice.models import User, Item, ItemOrder, Order
import random
from string import digits
from django.utils import timezone

MAX_ITEMS_PER_ORDER = 5


def get_random_date():
    return timezone.now() - timezone.timedelta(days=random.randint(0, 7))


def getRandomNumericString(n=8):
    return ''.join(random.choice(digits) for _ in range(n))


def get_random_txn_id():
    return f"TXN{getRandomNumericString()}"


def get_random_order_id():
    return f"OD{getRandomNumericString()}"


def generate_order_id():
    order_id = get_random_order_id()
    if Order.objects.filter(order_id=order_id).exists():
        return generate_order_id()
    return order_id


def createOrder(user, items):
    order_id = generate_order_id()
    placed_on = get_random_date()
    order_price = 0

    order = Order.objects.create(
        order_id=order_id,
        txn_id=get_random_txn_id(),
        placed_on=placed_on,
        price=0,
    )
    for item in items:
        delivery_timedelta = random.randint(1, 7)
        delivery_date = placed_on + timezone.timedelta(days=delivery_timedelta)
        return_valid_till = delivery_date + \
            timezone.timedelta(days=item.return_validity)
        exchange_valid_till = delivery_date + \
            timezone.timedelta(days=item.exchange_validity)

        if delivery_date > timezone.now():
            delivery_date = None
            return_valid_till = None
            exchange_valid_till = None

        itemOrder = ItemOrder.objects.create(
            item=item,
            user=user,
            order=order,
            price=item.sp,
            delivered_on=delivery_date,
            return_valid_till=return_valid_till,
            exchange_valid_till=exchange_valid_till,
        )

        order_price += itemOrder.price

    order.price = order_price
    order.save()

    print(f"Created order - {order.order_id}")


def populateOrders(n=50):
    users = User.objects.all()
    items = Item.objects.all()

    for _ in range(n):
        n_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        user = random.choice(users)
        item_list = [random.choice(items) for _ in range(n_items)]

        createOrder(user, item_list)
