from django.db import models
from django.contrib.auth.models import User

class DateTimeModel(models.Model):
    """ A base model with created and edited datetime fields """

    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(DateTimeModel):
    """ Public user profile """

    user = models.OneToOneField(User)
    picture = models.CharField(max_length=500)

    def get_full_name(self):
        full_name = self.user.first_name + ' ' + self.user.last_name
        return full_name if len(full_name) > 0 else self.user.username

    def __str__(self):
        return self.get_full_name()


class Person(DateTimeModel):
    """ Profile of someone who has been associated with shows """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "people"

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Show(DateTimeModel):
    """ A movie or television show """

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

    def __str__(self):
        return self.title


class Review(DateTimeModel):
    """ A personal review of a movie """

    score = models.PositiveSmallIntegerField()
    is_private = models.BooleanField(default=False)
    show = models.ForeignKey(Show)
    user = models.ForeignKey(UserProfile)

    class Meta:
        unique_together = ('show', 'user')

    def __str__(self):
        return '{}: {} by {}'.format(self.show, self.score, self.user)


class Group(DateTimeModel):
    """ A collection of users used for creating recommendation filters """

    title = models.CharField(max_length=50)
    users = models.ManyToManyField(
        UserProfile,
        related_name="friend_groups",
        blank=True
    )
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile)

    class Meta:
        unique_together = ('title', 'owner')

    def __str__(self):
        return self.title


class CuratedList(DateTimeModel):
    """ Collection of user curated shows  """

    title = models.CharField(max_length=100)
    shows = models.ManyToManyField(
        Show,
        related_name="curated_lists",
        blank=True
    )
    is_private = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile)
    followers = models.ManyToManyField(
        UserProfile,
        related_name="subscribed_lists",
        blank=True
    )

    class Meta:
        unique_together = ('title', 'owner')

    def __str__(self):
        return self.title
