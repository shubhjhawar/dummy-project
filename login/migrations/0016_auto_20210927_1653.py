# Generated by Django 3.0.6 on 2021-09-27 11:23

from django.db import migrations
import login.manager


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_customuser_user_status'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', login.manager.UserManager()),
            ],
        ),
    ]
