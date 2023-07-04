import requests
import json
import random
from WmVoice.models import Tag, Item, Category
from utils.add_data import RETURN_OR_EXCHANGE_VALIDITY_CHOICES
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files import File


CATEGORIES = {
    "Groceries": {
        "vegetables": [1, 2],
        "oils": [1],
        "pasta": [1],
        "milk": [1],
        "cake": [1],
    },
}


def populateItem(category, item_type, json_item):
    try:
        name = json_item.get('product_name')
        tag = item_type
        desc = json_item.get('labels')
        mrp = round(random.random() * 20, 2)
        sp = round(mrp * random.randint(70, 100)/100, 2)
        image_url = json_item.get('image_url')

        tag, _ = Tag.objects.get_or_create(name=tag)

        item = Item.objects.create(
            name=name,
            description=desc,
            category=category,
            mrp=mrp,
            sp=sp,
            return_validity=random.choice(RETURN_OR_EXCHANGE_VALIDITY_CHOICES),
            exchange_validity=random.choice(
                RETURN_OR_EXCHANGE_VALIDITY_CHOICES),
        )
        item.save()

        item.tags.add(tag)

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()
        item.image_1.save(f'items/{item.id}.png', File(img_temp))

        print(f"Added Item {item}")
    except:
        print(f"Skipping item : {json_item}")


def get_supermarket_items(item_type, page=1):
    url = f"https://fr-en.openfoodfacts.org/category/{item_type}/{page}.json"
    response = requests.get(url)
    data = json.loads(response.content).get("products")
    return data


def add_data_from_openfood():
    for category_name in CATEGORIES:
        category, _ = Category.objects.get_or_create(name=category_name)
        for item_type in CATEGORIES[category_name]:
            for page in CATEGORIES[category_name][item_type]:
                items = get_supermarket_items(item_type, page=page)
                for item in items:
                    populateItem(category, item_type, item)
