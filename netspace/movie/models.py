from django.db import models
# Create your models here.


class Movie(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, unique=True)
    director = models.CharField(max_length=255)
    screenwriter = models.CharField(max_length=255)
    actors = models.CharField(max_length=1000)
    category = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    initial = models.CharField(max_length=255)
    runtime = models.CharField(max_length=100)
    playUrl = models.CharField(max_length=1000)
    rate = models.CharField(max_length=255)
    starPeople = models.CharField(max_length=255)
    preShowUrl = models.CharField(max_length=255)
    intro = models.CharField(max_length=2555)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.title
