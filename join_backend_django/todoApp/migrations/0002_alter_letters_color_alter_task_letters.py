# Generated by Django 4.2.1 on 2023-05-24 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letters',
            name='color',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='letters',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='todoApp.letters'),
        ),
    ]