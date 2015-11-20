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

    full_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "people"

    def __str__(self):
        return self.full_name


class Show(DateTimeModel):
    """ A movie or television show """

    imdb_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    released = models.CharField(max_length=30, null=True, blank=True)
    plot = models.CharField(max_length=1000, null=True, blank=True)
    full_plot = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True)
    directors = models.ManyToManyField(
        Person,
        related_name="directions",
        blank=True
    )
    writers = models.ManyToManyField(
        Person,
        related_name="scripts",
        blank=True
    )
    banner = models.CharField(max_length=500, null=True, blank=True)
    poster = models.CharField(max_length=500, null=True, blank=True)
    background_color = models.CharField(max_length=10, default="#ffffff")
    text_color = models.CharField(max_length=10, default="#000000")
    detail_color = models.CharField(max_length=10, default="#ffffff")
    year = models.CharField(max_length=4, null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    runtime = models.CharField(max_length=50, null=True, blank=True)
    cast = models.ManyToManyField(
        Person,
        related_name="portfolio",
        blank=True
    )
    metacritic = models.PositiveSmallIntegerField(null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    imdb_votes = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    awards = models.CharField(max_length=200, null=True, blank=True)
    last_updated = models.DateTimeField()
    type = models.CharField(max_length=20)

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
