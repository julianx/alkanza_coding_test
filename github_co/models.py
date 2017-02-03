from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RepoManager(models.Manager):
    def get_popular_repos(self):
        return self.filter().order_by('-stars')[10]

    def get_colombian_repos(self):
        return self.filter(User__location__name__contains="Colombia")

    def get_popular_colombian_repos(self):
        return self.filter().order_by('-contributors')[10]


class Repos(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField()
    contributors = models.ManyToManyField('User', related_name='contributors', null=True, blank=True)

    def __str__(self):
        return "%s, Star gazers: %d" % (self.name, self.stars)


class User(models.Model):
    username = models.CharField(max_length=100)
    repos = models.ManyToManyField(Repos)
    location = models.ForeignKey(Location)
    colombian = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
