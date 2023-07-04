import json
import random
import ssl
import urllib.request
from WmVoice.models import Category, Item, Tag
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

RETURN_OR_EXCHANGE_VALIDITY_CHOICES = [0, 1, 3, 7]

CATEGORIES = {
    'Clothing': [
        # 'assets/clothing.json',
    ],
    'Groceries': [
        'assets/groceries.json',
        'assets/groceries2.json',
        'assets/groceries3.json',
    ],
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def populateItemsGroceries1(category, filename):

    content = json.loads(open(filename, 'r').read())
    content = list(content)

    IMAGE_ROOT = "https://raw.githubusercontent.com/wedeploy-examples/supermarket-web-example/master/ui/assets/images/"
    for json_item in content:
        if True:
            name = json_item.get('title')
            tag = json_item.get('type')
            desc = json_item.get('description')
            mrp = round(random.random() * 20, 2)
            sp = round(mrp * random.randint(70, 100)/100, 2)
            image_url = IMAGE_ROOT + json_item.get('filename')

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
            img_temp.write(urlopen(image_url, context=ctx).read())
            img_temp.flush()
            item.image_1.save(f'items/{item.id}.png', File(img_temp))

            print(f"Added Item {item}")
        # except:
        #     print(f"Error occurred, skipping {json_item}")


def populateItemsGroceries2(category, filename):

    content = json.loads(open(filename, 'r').read())
    content = list(content)

    IMAGE_ROOT = "https://raw.githubusercontent.com/ParasGarg/Online-Grocery-Store/master"
    for json_item in content:
        try:
            name = json_item.get('title')
            tag = json_item.get('category')
            desc = json_item.get('description')
            mrp = round(random.random() * 20, 2)
            sp = round(mrp * random.randint(70, 100)/100, 2)
            images = json_item.get('images')
            if len(images) > 0:
                image_url = IMAGE_ROOT + images[0]

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

            if len(images) > 0:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(image_url).read())
                img_temp.flush()
                item.image_1.save(f'items/{item.id}.png', File(img_temp))

            print(f"Added Item {item}")
        except:
            print(f"Error occurred, skipping {json_item}")


def populateItemsGroceries3(category, filename):

    content = json.loads(open(filename, 'r').read())
    content = list(content)

    IMAGE_ROOT = "https://raw.githubusercontent.com/yZipperer/item-api/main/images/"
    for json_item in content:
        try:
            name = json_item.get('name')
            tag = json_item.get('category')
            desc = json_item.get('ingredients')
            mrp = round(random.random() * 20, 2)
            sp = round(mrp * random.randint(70, 100)/100, 2)
            image_url = IMAGE_ROOT + json_item.get('image').split('/')[-1]

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

            try:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(image_url).read())
                img_temp.flush()
                item.image_1.save(f'items/{item.id}.png', File(img_temp))
            except Exception:
                if '.jpeg' in image_url:
                    image_url = image_url.replace('.jpeg', '.jpg')
                elif '.jpg' in image_url:
                    image_url = image_url.replace('.jpg', '.jpeg')
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(image_url).read())
                img_temp.flush()
                item.image_1.save(f'items/{item.id}.png', File(img_temp))

            print(f"Added Item {item}")
        except:
            print(f"Error occurred, skipping {json_item}")


def populateData():
    for category_name, files in CATEGORIES.items():
        category, _ = Category.objects.get_or_create(name=category_name)
        for file in files:
            if file == 'assets/groceries.json':
                populateItemsGroceries1(category, file)
            elif file == 'assets/groceries2.json':
                populateItemsGroceries2(category, file)
            elif file == 'assets/groceries3.json':
                populateItemsGroceries3(category, file)
