# Generated by Django 4.2.1 on 2023-06-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0019_alter_task_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='contactNames',
            field=models.ManyToManyField(to='todoApp.contact'),
        ),
    ]
