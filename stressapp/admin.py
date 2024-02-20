from django.contrib import admin
from .models import userAttribute, interest, friend_request, chat, message

# Register your models here.
admin.site.register(interest)

admin.site.register(userAttribute)

admin.site.register(friend_request)

admin.site.register(chat)

admin.site.register(message)
