from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)


class Repos(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField()
    contributors = models.ManyToManyField('User', related_name='contributors')

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=100)
    repos = models.ManyToManyField(Repos)
    location = models.ForeignKey(Location)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
