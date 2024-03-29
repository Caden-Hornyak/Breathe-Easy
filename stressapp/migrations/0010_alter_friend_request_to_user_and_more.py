# Generated by Django 4.2.6 on 2024-02-21 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stressapp', '0009_remove_friend_request_to_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='to_user',
            field=models.ManyToManyField(blank=True, related_name='to_user', to='stressapp.userattribute'),
        ),
        migrations.AlterField(
            model_name='userattribute',
            name='chats',
            field=models.ManyToManyField(blank=True, related_name='chats', to='stressapp.chat'),
        ),
    ]
