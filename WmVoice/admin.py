from django.contrib import admin
from .models import User, Tag, Category, Item, ItemCart, ItemVisit, ItemOrder, Order, Review


for model in [User, Tag, Category, Item, ItemCart, ItemVisit, ItemOrder, Order, Review]:
    admin.site.register(model)
