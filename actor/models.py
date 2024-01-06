from django.db import models
from django.utils.text import slugify
# Create your models here.


class Actor(models.Model):
    Name = models.CharField(max_length=70, unique=True)
    Picture = models.ImageField(blank=True)
    Slug = models.SlugField(null=True, unique=True)
    Movies = models.ManyToManyField('movie.Movie')

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.Slug:
            self.Slug = slugify(self.Name)
        return super().save(*args, **kwargs)
