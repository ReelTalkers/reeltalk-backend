import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField
from graphql.core.type import GraphQLArgument, GraphQLString
import re

from . import models

schema = graphene.Schema(name='ReelTalk Relay Schema')


class Connection(relay.Connection):
    total_count = graphene.IntField()

    def resolve_total_count(self, args, info):
        print(dir(self))
        return len(self.get_connection_data())


class Review(DjangoNode):
    class Meta:
        model = models.Review
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Show(DjangoNode):
    reviews = relay.ConnectionField(
        Review, description='Reviews this show has received'
    )

    @resolve_only_args
    def resolve_reviews(self, **args):
        return self.instance.review_set.all()

    class Meta:
        model = models.Show
        exclude_fields = ('created', 'edited', 'review')

    connection_type = Connection


class Person(DjangoNode):
    portfolio = relay.ConnectionField(
        Show, description='Shows in which this person is involved'
    )

    @resolve_only_args
    def resolve_portfolio(self, *args):
        return self.instance.show_set.all()

    class Meta:
        model = models.Person
        exclude_fields = ('created', 'edited', 'show')

    connection_type = Connection


class User(DjangoNode):
    class Meta:
        model = models.User
        exclude_fields = ('created', 'edited', 'password')

    connection_type = Connection


class CuratedList(DjangoNode):
    class Meta:
        model = models.CuratedList
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Group(DjangoNode):
    class Meta:
        model = models.Group
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class UserProfile(DjangoNode):
    subscribed_lists = relay.ConnectionField(
        CuratedList, description='Curated lists this user is following'
    )
    groups = relay.ConnectionField(
        Group, description='Groups this user has made'
    )
    reviews = relay.ConnectionField(
        Review, description='Reviews this user has crafted'
    )

    @resolve_only_args
    def resolve_subscribed_lists(self, **args):
        return self.instance.curatedlist_set.all()

    @resolve_only_args
    def resolve_groups(self, **args):
        return self.instance.friend_groups.all()

    @resolve_only_args
    def resolve_reviews(self, **args):
        return self.instance.review_set.all()

    class Meta:
        model = models.UserProfile
        exclude_fields = ('created', 'edited', 'curatedlist', 'group', 'review')


def get_filterable_fields(model):
    is_valid = lambda field: not field.is_relation and field.name not in ['created', 'edited', 'id']
    return [field.name for field in model._meta.get_fields() if is_valid(field) ]

def get_graphql_filter_arguments(fields):
    return { to_camel_case(field): GraphQLArgument(GraphQLString) for field in fields }

def extract_model_fields(model, all_fields):
    return {to_snake_case(k):v for k, v in all_fields.items() if to_snake_case(k) in get_filterable_fields(model)}

def to_camel_case(term):
   first, *rest = term.split('_')
   return first + ''.join(word.capitalize() for word in rest)

def to_snake_case(term):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', term)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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
    curated_list = relay.NodeField(CuratedList)
    group = relay.NodeField(Group)
    node = relay.NodeField()
    viewer = graphene.Field('self')
    filter_curated_lists = relay.ConnectionField(
        CuratedList,
        **get_graphql_filter_arguments(get_filterable_fields(models.CuratedList))
    )
    filter_groups = relay.ConnectionField(
        Group,
        **get_graphql_filter_arguments(get_filterable_fields(models.Group))
    )
    filter_people = relay.ConnectionField(
        Person,
        **get_graphql_filter_arguments(get_filterable_fields(models.Person))
    )
    filter_reviews = relay.ConnectionField(
        Review,
        **get_graphql_filter_arguments(get_filterable_fields(models.Review))
    )
    filter_shows = relay.ConnectionField(
        Show,
        **get_graphql_filter_arguments(get_filterable_fields(models.Show))
    )
    filter_user_profiles = relay.ConnectionField(
        UserProfile,
        **get_graphql_filter_arguments(get_filterable_fields(models.UserProfile))
    )

    @resolve_only_args
    def resolve_filter_curated_lists(self, **kwargs):
        model_filters = extract_model_fields(models.CuratedList, kwargs)
        return models.CuratedList.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_filter_groups(self, **kwargs):
        model_filters = extract_model_fields(models.Group, kwargs)
        return models.Group.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_filter_people(self, **kwargs):
        model_filters = extract_model_fields(models.Person, kwargs)
        return models.Person.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_filter_reviews(self, **kwargs):
        model_filters = extract_model_fields(models.Review, kwargs)
        return models.Review.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_filter_shows(self, **kwargs):
        model_filters = extract_model_fields(models.Show, kwargs)
        return models.Show.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_filter_user_profiles(self, **kwargs):
        model_filters = extract_model_fields(models.UserProfile, kwargs)
        return models.UserProfile.objects.filter(**model_filters)

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
