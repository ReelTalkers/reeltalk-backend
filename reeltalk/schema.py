import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField
from graphql_relay.node.node import from_global_id
from graphql.core.type import (
    GraphQLArgument,
    GraphQLString,
    GraphQLInt,
    GraphQLFloat,
    GraphQLBoolean,
    GraphQLList
)
import re

from . import models
from .filter_shows import get_show_recommendations_via_group

schema = graphene.Schema(name='ReelTalk Relay Schema')


class Connection(relay.Connection):
    total_count = graphene.IntField()

    def resolve_total_count(self, args, info):
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


def get_filterable_fields(model, accept_relations=True):
    is_proper_relation = lambda field: accept_relations and field.one_to_one
    is_valid = lambda field: is_proper_relation(field) if field.is_relation else True
    is_excluded = lambda field: field.name in ['created', 'edited', 'id']
    return [field for field in model._meta.get_fields() if is_valid(field) and not is_excluded(field) ]

def get_graphql_type(field):
    field_type = field.get_internal_type()
    if 'Integer' in field_type:
        return GraphQLInt
    elif 'Decimal' in field_type:
        return GraphQLFloat
    elif 'Boolean' in field_type:
        return GraphQLBoolean
    else:
        return GraphQLString

def get_graphql_filter_arguments(fields):
    filter_args = {}
    for field in fields:
        if field.is_relation:
            for related_field in get_filterable_fields(field.related_model, accept_relations=False):
                key = '{}__{}'.format(field.name, related_field.name)
                graphql_type = get_graphql_type(related_field)
                if graphql_type == GraphQLString:
                    filter_args['{}__{}'.format(key, 'contains')] = GraphQLArgument(graphql_type)
                filter_args[key] = GraphQLArgument(graphql_type)
        else:
            graphql_type = get_graphql_type(field)
            if graphql_type == GraphQLString:
                filter_args['{}__{}'.format(field.name, 'contains')] = GraphQLArgument(graphql_type)
            filter_args[field.name] = GraphQLArgument(get_graphql_type(field))
    return filter_args

def extract_model_filters(model, all_fields):
    model_filters = {}
    for k, v in all_fields.items():
        field_name = k
        if '__' in k:
            model_filters[field_name] = v
            continue
        if field_name in [field.name for field in get_filterable_fields(model)]:
            model_filters[field_name] = v
    return model_filters


class ReviewShow(relay.ClientIDMutation):
    class Input:
        score = graphene.IntField(required=True)
        show_id = graphene.StringField(required=True)
        user_profile_id = graphene.StringField(required=True)

    review = graphene.Field(Review)
    show = graphene.Field(Show)
    user_profile = graphene.Field(UserProfile)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        score = input.get('score')
        show_id = input.get('show_id')
        user_profile_id = input.get('user_profile_id')

        show = models.Show.objects.get(id=from_global_id(show_id).id)
        user_profile = models.UserProfile.objects.get(id=from_global_id(user_profile_id).id)
        review, created = models.Review.objects.update_or_create(
            user=user_profile,
            show=show,
            defaults={'score': score}
        )
        return ReviewShow(review=review, show=show, user_profile=user_profile)


class Query(graphene.ObjectType):
    all_shows = DjangoConnectionField(
        Show,
        **get_graphql_filter_arguments(get_filterable_fields(models.Show))
    )
    all_reviews = DjangoConnectionField(
        Review,
        **get_graphql_filter_arguments(get_filterable_fields(models.Review))
    )
    all_user_profiles = DjangoConnectionField(
        UserProfile,
        **get_graphql_filter_arguments(get_filterable_fields(models.UserProfile))
    )
    all_groups = DjangoConnectionField(
        Group,
        **get_graphql_filter_arguments(get_filterable_fields(models.Group))
    )
    all_people = DjangoConnectionField(
        Person,
        **get_graphql_filter_arguments(get_filterable_fields(models.Person))
    )
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
    recommend_shows = DjangoConnectionField(
        Show,
        user_ids=GraphQLArgument(GraphQLList(GraphQLString))
    )

    @resolve_only_args
    def resolve_all_curated_lists(self, **kwargs):
        model_filters = extract_model_filters(models.CuratedList, kwargs)
        return models.CuratedList.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_all_groups(self, **kwargs):
        model_filters = extract_model_filters(models.Group, kwargs)
        return models.Group.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_all_people(self, **kwargs):
        model_filters = extract_model_filters(models.Person, kwargs)
        return models.Person.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_all_reviews(self, **kwargs):
        model_filters = extract_model_filters(models.Review, kwargs)
        return models.Review.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_all_shows(self, **kwargs):
        model_filters = extract_model_filters(models.Show, kwargs)
        return models.Show.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_all_user_profiles(self, **kwargs):
        model_filters = extract_model_filters(models.UserProfile, kwargs)
        return models.UserProfile.objects.filter(**model_filters)

    @resolve_only_args
    def resolve_recommend_shows(self, user_ids=None, **kwargs):
        if user_ids:
            user_profile_ids = [from_global_id(g_id).id for g_id in user_ids]
            group = models.UserProfile.objects.filter(id__in=user_profile_ids)
            all_users = models.UserProfile.objects.all() # TODO: eventually query user's friends
            return get_show_recommendations_via_group(group, all_users)
        else:
            return models.Show.objects.all()

    def resolve_viewer(self, *args, **kwargs):
        return self

class Mutation(graphene.ObjectType):
    review_show = graphene.Field(ReviewShow)

schema.query = Query
schema.mutation = Mutation

import json

introspection_dict = schema.introspect()

print(json.dumps(introspection_dict))
