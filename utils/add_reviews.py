from WmVoice.models import Item, Review, User
import pandas as pd
import random


FILENAME = "assets/Reviews.csv"
MAX_REVIEWS = 1000


def getUsers():
    return User.objects.all()


def getItems():
    return Item.objects.all()


def assignReview(item, user, reviewText, score):
    try:
        review = Review.objects.create(
            rating=int(score),
            comment=reviewText,
            item=item,
            user=user,
        )
        print(f"Added review : {review.comment}")
    except Exception as e:
        print(f"Error while adding review. Exception trace : {e}")


def populateReviews():
    items = list(getItems())
    users = list(getUsers())
    reviews = list(pd.read_csv(FILENAME)['Text'])
    scores = list(pd.read_csv(FILENAME)['Score'])

    for i, (score, review) in enumerate(zip(scores, reviews)):
        if i == MAX_REVIEWS:
            break
        item = random.choice(items)
        user = random.choice(users)
        assignReview(item, user, review, score)

    for item in Item.objects.all():
        item.refreshRating()
