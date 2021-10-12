# Generated by Django 3.0.6 on 2021-09-27 11:23

from django.db import migrations, models
import login.manager


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_auto_20210927_1651'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', login.manager.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_status',
            field=models.CharField(choices=[('0', 'employee'), ('1', 'manager')], default='employee', max_length=20),
        ),
    ]
