# Generated by Django 4.2.1 on 2023-06-04 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0020_alter_task_contactnames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='contactNames',
            field=models.ManyToManyField(to='todoApp.users'),
        ),
    ]
