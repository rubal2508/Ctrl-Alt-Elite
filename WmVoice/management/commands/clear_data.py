from django.core.management.base import BaseCommand, CommandError
from WmVoice.models import User, Tag, Category, Item, ItemCart, ItemVisit, ItemOrder, Order, Review


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in [User, Tag, Category, Item, ItemCart, ItemVisit, ItemOrder, Order, Review]:
            model.objects.all().delete()
            print(f"Cleaned model {model}")
