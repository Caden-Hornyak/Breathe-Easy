from django.db import models
import uuid
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
    profile_picture = models.ImageField(default='default_profpic.png')
    chats = models.ManyToManyField('chat', blank=True, related_name='chats')

    def __str__(self):
        return self.username

class friend_request(models.Model):
    from_user = models.ForeignKey(userAttribute, blank=True, null=True, related_name='from_user', on_delete=models.SET_NULL)
    to_user = models.ManyToManyField(userAttribute, blank=True, related_name='to_user')

    def __str__(self):
        return self.from_user + " request to " + self.to_user


class message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(userAttribute, blank=True, null=True, related_name='user', on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.text


class chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(userAttribute, related_name='participants')
    date_created = models.DateTimeField(auto_now_add=True)
    chat_messages = models.ManyToManyField(message, blank=True, related_name='chat_messages')

    def __str__(self):
        return ''.join(str(self.participants))
