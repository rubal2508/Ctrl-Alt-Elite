from django.core.management.base import BaseCommand, CommandError
from utils.add_data import populateData
from utils.openFoodApi import add_data_from_openfood
from utils.add_users import populateUsers
from utils.add_reviews import populateReviews
from utils.add_orders import populateOrders
from utils.demo_data import populateDemoProductAndReviews


class Command(BaseCommand):

    def handle(self, *args, **options):
        populateData()
        add_data_from_openfood()
        populateUsers()
        populateReviews()
        populateOrders()
        populateDemoProductAndReviews()
        pass
