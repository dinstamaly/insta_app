# Generated by Django 3.1.7 on 2021-04-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='count_likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
