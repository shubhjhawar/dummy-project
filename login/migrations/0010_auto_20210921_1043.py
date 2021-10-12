# Generated by Django 3.0.6 on 2021-09-21 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_remove_remarkmodel_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='remarkmodel',
            old_name='remarks',
            new_name='remark',
        ),
        migrations.RemoveField(
            model_name='remarkmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='remarkmodel',
            name='task',
            field=models.ManyToManyField(to='login.TaskModel'),
        ),
    ]
