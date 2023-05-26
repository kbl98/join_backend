# Generated by Django 4.2.1 on 2023-05-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0011_task_subtask_alter_task_contactnames'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, help_text='Contact phone number', max_length=18),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(blank=True, help_text='Contact phone number', max_length=18, null=True),
        ),
    ]
