from django.db import models
from django.utils.text import slugify
from django.core import files
from actor.models import Actor
import requests
from io import BytesIO

# Create your models here.


class Genre(models.Model):
    Title = models.CharField(max_length=25)
    Slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if not self.Slug:
            self.Title.replace('', '')
            self.Slug = slugify(self.Title)
        return super().save(*args, **kwargs)


class Rating(models.Model):
    Source = models.CharField(max_length=50)
    Rating = models.CharField(max_length=10)

    def __str__(self):
        return self.Source


class Movie(models.Model):
    Title = models.CharField(max_length=200)
    Year = models.CharField(max_length=25, blank=True)
    Rated = models.CharField(max_length=10, blank=True)
    Released = models.CharField(max_length=25, blank=True)
    Runtime = models.CharField(max_length=25, blank=True)
    Genre = models.ManyToManyField(Genre, blank=True)
    Director = models.CharField(max_length=100, blank=True)
    Writer = models.CharField(max_length=300, blank=True)
    Actors = models.ManyToManyField(Actor, blank=True)
    Plot = models.CharField(max_length=900, blank=True)
    Language = models.CharField(max_length=300, blank=True)
    Country = models.CharField(max_length=100, blank=True)
    Awards = models.CharField(max_length=250, blank=True)
    Poster = models.ImageField(upload_to='movies', blank=True)
    Poster_url = models.URLField(blank=True)
    Ratings = models.ManyToManyField(Rating, blank=True)
    Metascore = models.CharField(max_length=5, blank=True)
    imdbRating = models.CharField(max_length=5, blank=True)
    imdbVotes = models.CharField(max_length=100, blank=True)
    imdbID = models.CharField(max_length=100, blank=True)
    Type = models.CharField(max_length=10, blank=True)
    DVD = models.CharField(max_length=25, blank=True)
    BoxOffice = models.CharField(max_length=25, blank=True)
    Production = models.CharField(max_length=100, blank=True)
    Website = models.CharField(max_length=150, blank=True)
    totalSeasons = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if self.Poster == '' and self.Poster_url != '':
            resp = requests.get(self.Poster_url)
            pb = BytesIO()
            pb.write(resp.content)
            pb.flush()
            file_name = self.Poster_url.split("/")[-1]
            self.Poster.save(file_name, files.File(pb), save=False)
        return super().save(*args, **kwargs)