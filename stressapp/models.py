from django.db import models

# Create your models here.

class interest(models.Model):
    interest = models.CharField(max_length=100)

    def __str__(self):
        return self.interest

class userAttribute(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    tags = models.ManyToManyField(interest)
    new_user = models.BooleanField(default=True)
    remember_me = models.BooleanField(default=False)
    friends = models.ManyToManyField("userAttribute", blank=True)

    def __str__(self):
        return self.username

class friend_request(models.Model):
    from_user = models.ForeignKey(userAttribute, null=True, related_name='from_user', on_delete=models.SET_NULL)
    to_user = models.ForeignKey(userAttribute, null=True, related_name='to_user', on_delete=models.SET_NULL)