from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Studio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Distributor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    box_art = models.ImageField(upload_to='box_art/', default='box_art/default_boxart.jpg')
    studios = models.ManyToManyField(Studio, related_name='games')
    publishers = models.ManyToManyField(Publisher, related_name='games')
    distributors = models.ManyToManyField(Distributor, related_name='games')
    platforms = models.ManyToManyField(Platform, related_name='games')
    genres = models.ManyToManyField(Genre, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
