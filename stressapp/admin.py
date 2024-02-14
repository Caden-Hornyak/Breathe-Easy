from django.contrib import admin
from .models import userAttribute, interest

# Register your models here.
admin.site.register(interest)

@admin.register(userAttribute)
class BookAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname')
