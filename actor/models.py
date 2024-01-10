from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.


class Actor(models.Model):
    Name = models.CharField(max_length=70, unique=True)
    Picture = models.ImageField(blank=True)
    slug = models.SlugField(null=True, unique=True)
    Movies = models.ManyToManyField('movie.Movie')

    def get_absolute_url(self):
        return reverse('actors', args=[self.slug])

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Name)
        return super().save(*args, **kwargs)
