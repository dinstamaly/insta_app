# Generated by Django 3.1.7 on 2021-04-29 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countryview',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country.country'),
        ),
    ]
