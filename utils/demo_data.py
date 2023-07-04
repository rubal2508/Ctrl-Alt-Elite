from WmVoice.models import Item, Tag, Review, User, Category
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
import random
import json
import ssl


DEMO_PRODUCT_JSON_FILE = "assets/demo/Item.json"
DEMO_REVIEWS_JSON_FILE = "assets/demo/Reviews.json"

CATEGORY, _ = Category.objects.get_or_create(name="Clothing")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def populateReview(item, user, review):
    rating = review.get('Rating')
    comment = review.get('Comment')

    Review.objects.create(
        rating=rating,
        comment=comment,
        item=item,
        user=user
    )
    print(f"Added review : {review}")


def populateReviews(item):

    content = json.loads(open(DEMO_REVIEWS_JSON_FILE, 'r').read())
    reviews = list(content)

    users = User.objects.all()

    for review in reviews:
        user = random.choice(users)
        populateReview(item, user, review)


def populateProduct():

    content = json.loads(open(DEMO_PRODUCT_JSON_FILE, 'r').read())

    name = content.get('Name')
    description = content.get('Description')
    image_url = content.get('Image 1')
    mrp = content.get('Mrp')
    sp = content.get('Sp')
    tags = content.get('Tags')
    return_validity = content.get('Return validity')
    exchange_validity = content.get('Exchange validity')

    item = Item.objects.create(
        name=name,
        description=description,
        category=CATEGORY,
        mrp=mrp,
        sp=sp,
        return_validity=return_validity,
        exchange_validity=exchange_validity,
    )

    for tag in tags:
        tag_object, _ = Tag.objects.get_or_create(name=tag)
        item.tags.add(tag_object)

    # return product
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_url, context=ctx).read())
    img_temp.flush()
    item.image_1.save(f'items/{item.id}.png', File(img_temp))

    print(f"Added Item {item}")

    return item


def populateDemoProductAndReviews():
    item = populateProduct()
    populateReviews(item)
    item.refreshRating()
