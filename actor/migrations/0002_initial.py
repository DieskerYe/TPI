# Generated by Django 5.0 on 2024-01-12 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actor', '0001_initial'),
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='Movies',
            field=models.ManyToManyField(to='movie.movie'),
        ),
    ]