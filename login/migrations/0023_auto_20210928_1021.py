# Generated by Django 3.0.6 on 2021-09-28 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_auto_20210927_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_status',
            field=models.CharField(choices=[('0', 'employee'), ('1', 'manager')], default='employee', max_length=20),
        ),
    ]
