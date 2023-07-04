from django.db import models
from statistics import mean
from django.templatetags.static import static


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):

    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(default=0.0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='choice_items')
    image_1 = models.ImageField(null=True, blank=True)
    image_2 = models.ImageField(null=True, blank=True)
    image_3 = models.ImageField(null=True, blank=True)
    image_4 = models.ImageField(null=True, blank=True)
    image_5 = models.ImageField(null=True, blank=True)
    image_6 = models.ImageField(null=True, blank=True)
    mrp = models.DecimalField(decimal_places=2, max_digits=10)
    sp = models.DecimalField(decimal_places=2, max_digits=10)

    tags = models.ManyToManyField(
        Tag, related_name='choice_items', blank=True)

    return_validity = models.IntegerField(default=7)
    exchange_validity = models.IntegerField(default=7)

    def __str__(self):
        return self.name

    def getReviewCount(self):
        return self.choice_reviews.count()

    def refreshRating(self):
        if self.choice_reviews.count() == 0:
            return
        self.rating = mean(
            [review.rating for review in self.choice_reviews.all()])
        self.save()

    def getImageUrl(self):
        if self.image_1:
            return self.image_1.url
        return static('images/no-image.png')

    def getReviewsInLinedStrings(self):
        return '\n'.join([review.comment for review in self.choice_reviews.all()])
