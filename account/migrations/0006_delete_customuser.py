# Generated by Django 4.2.5 on 2023-12-09 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_customuser_user_comments'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]