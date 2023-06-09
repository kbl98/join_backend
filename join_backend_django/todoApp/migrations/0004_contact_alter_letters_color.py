# Generated by Django 4.2.1 on 2023-05-24 19:48

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0003_alter_task_letters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('color', models.CharField(default='#ffffff', max_length=7)),
            ],
        ),
        migrations.AlterField(
            model_name='letters',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
