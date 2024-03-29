from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core import files
from django.urls import reverse
from actor.models import Actor
import requests
from io import BytesIO

# Create your models here.


class Genre(models.Model):
    Title = models.CharField(max_length=25)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('genres', args=[self.slug])

    def __str__(self):
        return self.Title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.Title.replace('', '')
            self.slug = slugify(self.Title)
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


RATE_OPCIONES = [
    (1, '1- Basura'),
    (2, '2- Horrible'),
    (3, '3- Terrible'),
    (4, '4- Mala'),
    (5, '5- OK'),
    (6, '6- Mirable'),
    (7, '7- Buena'),
    (8, '8- Muy buena'),
    (9, '9- Casi perfecta'),
    (10, '10- Obra maestra')
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=3000, blank=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_OPCIONES)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    type_like = models.PositiveSmallIntegerField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_like')
