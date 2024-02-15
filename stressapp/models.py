from django.db import models

# Create your models here.

class interest(models.Model):
    interest = models.CharField(max_length=100)

    def __str__(self):
        return self.interest

class userAttribute(models.Model):
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tags = models.ManyToManyField(interest)
    new_user = models.BooleanField(default=True)

    def __str__(self):
        return self.username
