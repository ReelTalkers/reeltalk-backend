from django.db import models
from django.contrib.auth.models import User

class DateTimeModel(models.Model):
    """ A base model with created and edited datetime fields """

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(DateTimeModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "people"


class Show(DateTimeModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    genre = models.CharField(max_length=50)
    director = models.ForeignKey(Person)
    banner = models.CharField(max_length=500)
    poster = models.CharField(max_length=500)
    background_color = models.CharField(max_length=10, default="#ffffff")
    text_color = models.CharField(max_length=10, default="#000000")
    detail_color = models.CharField(max_length=10, default="#ffffff")
    year = models.CharField(max_length=4)
    mpaa_rating = models.CharField(max_length=20)
    runtime = models.CharField(max_length=50)
    actors = models.ManyToManyField(
        Person,
        related_name="portfolio",
        blank=True
    )


class Review(DateTimeModel):
    score = models.PositiveSmallIntegerField()
    show = models.ForeignKey(Show)
    user = models.ForeignKey(User)


class Group(DateTimeModel):
    title = models.CharField(max_length=50)
    users = models.ManyToManyField(
        User,
        related_name="friend_groups",
        blank=True
    )

class UserProfile(DateTimeModel):
    user = models.OneToOneField(User)
    picture = models.CharField(max_length=500)
