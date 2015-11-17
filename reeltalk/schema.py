import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField

from . import models

schema = graphene.Schema(name='ReelTalk Relay Schema')


class Connection(relay.Connection):
    total_count = graphene.IntField()

    def resolve_total_count(self, args, info):
        return len(self.get_connection_data())


class Person(DjangoNode):
    class Meta:
        model = models.Person
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Show(DjangoNode):
    class Meta:
        model = models.Show
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Review(DjangoNode):
    class Meta:
        model = models.Review
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class User(DjangoNode):
    class Meta:
        model = models.User
        exclude_fields = ('created', 'edited', 'password')

    connection_type = Connection


class UserProfile(DjangoNode):
    class Meta:
        model = models.UserProfile
        exclude_fields = ('created', 'edited')


class Group(DjangoNode):
    class Meta:
        model = models.Group
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class CuratedList(DjangoNode):
    class Meta:
        model = models.CuratedList
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Query(graphene.ObjectType):
    all_shows = DjangoConnectionField(Show)
    all_reviews = DjangoConnectionField(Review)
    all_users = DjangoConnectionField(User)
    all_user_profiles = DjangoConnectionField(UserProfile)
    all_groups = DjangoConnectionField(Group)
    all_people = DjangoConnectionField(Person)
    all_curated_lists = DjangoConnectionField(CuratedList)
    person = relay.NodeField(Person)
    show = relay.NodeField(Show)
    review = relay.NodeField(Review)
    user = relay.NodeField(User)
    user_profile = relay.NodeField(UserProfile)
    group = relay.NodeField(Group)
    node = relay.NodeField()
    viewer = graphene.Field('self')

    @resolve_only_args
    def resolve_all_shows(self, **kwargs):
        return models.Show.objects.all()

    @resolve_only_args
    def resolve_all_reviews(self, **kwargs):
        return models.Review.objects.all()

    @resolve_only_args
    def resolve_all_users(self, **kwargs):
        return models.User.objects.all()

    @resolve_only_args
    def resolve_all_user_profiles(self, **kwargs):
        return models.UserProfile.objects.all()

    @resolve_only_args
    def resolve_all_people(self, **kwargs):
        return models.Person.objects.all()

    @resolve_only_args
    def resolve_all_groups(self, **kwargs):
        return models.Group.objects.all()

    @resolve_only_args
    def resolve_all_curated_lists(self, **kwargs):
        return models.CuratedList.objects.all()

    def resolve_viewer(self, *args, **kwargs):
        return self


schema.query = Query

import json

introspection_dict = schema.introspect()

print(json.dumps(introspection_dict))
