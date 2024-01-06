from django.db import models
from django.utils.text import slugify
from django.core import files
from actor.models import Actor
import requests
from io import BytesIO

# Create your models here.

class Genre(models.Model):
    title = models.CharField(max_length=25)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.title.replace('', '')
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Rating(models.Model):
    source = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.source

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=25, blank=True)
    rated = models.CharField(max_length=25, blank=True)
    released = models.CharField(max_length=25, blank=True)
    runtime = models.ManyToManyField(Genre, blank=True)
    director = models.CharField(max_length=100, blank=True)
    writer = models.CharField(max_length=300, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    plot = models.CharField(max_length=900, blank=True)
    language = models.CharField(max_length=300, blank=True)
    country = models.CharField(max_length=100, blank=True)
    awards = models.CharField(max_length=250, blank=True)
    poster = models.ImageField(upload_to='movies', blank=True)
    poster_url = models.URLField(blank=True)
    ratings = models.ManyToManyField(Rating, blank=True)
    metascore = models.CharField(max_length=5, blank=True)
    imdb_rating = models.CharField(max_length=5, blank=True)
    imdb_votes = models.CharField(max_length=100, blank=True)
    imdb_id = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, blank=True)
    dvd = models.CharField(max_length=25, blank=True)
    box_office = models.CharField(max_length=25, blank=True)
    production = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=150, blank=True)

    totalSeasons = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.poster == '' and self.poster_url != '':
            resp = requests.get(self.poster_url)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.poster_url.split("/")[-1]
            self.poster.save(file_name, files.File(pb), save=False)
        return super().save(*args, **kwargs)
