import json
from django.db import models
from django.utils import timezone
from WmVoice.models.choices import RATING_CHOICES, RETURN_STATUS_CHOICES
from WmVoice.models.items import Item
from WmVoice.models.users import User


class ItemCart(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='choice_cart_items')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='choice_cart_items')
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.name} - {self.item.name}"


class ItemVisit(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='choice_visits')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='choice_visits')
    last_visit = models.DateTimeField(default=timezone.now)
    visit_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.name} - {self.last_visit}"


class Order(models.Model):

    order_id = models.CharField(unique=True, max_length=50)
    txn_id = models.CharField(max_length=50)
    placed_on = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.order_id} - {self.price}"


class ItemOrder(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='choice_orders')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='choice_ordered_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='choice_ordered_items')
    price = models.DecimalField(decimal_places=2, max_digits=10)

    delivered_on = models.DateTimeField(null=True, blank=True)
    return_valid_till = models.DateTimeField(null=True, blank=True)
    exchange_valid_till = models.DateTimeField(null=True, blank=True)

    return_status = models.CharField(max_length=20,
                                     choices=RETURN_STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.item}"

    def getAgentJson(self):
        return json.dump({"id": self.id, "name": self.item.name})

    def initiateReturn(self):
        self.return_status = 'Return Initiated'
        self.save()


class Review(models.Model):

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(null=True, blank=True)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='choice_reviews')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='choice_reviews',
        null=True, blank=True)

    image_1 = models.ImageField(null=True, blank=True)
    image_2 = models.ImageField(null=True, blank=True)
    image_3 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.rating} - {self.item}"
