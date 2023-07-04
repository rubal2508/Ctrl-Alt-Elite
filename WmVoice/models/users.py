from django.db import models
from django.utils import timezone


class User(models.Model):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    password = models.CharField(max_length=256)
    created_on = models.DateTimeField(default=timezone.now)
    birthday = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
