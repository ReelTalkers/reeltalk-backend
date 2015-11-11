import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField

from .models import User, Show, Review, Group


schema = graphene.Schema(name='ReelTalk Relay Schema')


class Connection(relay.Connection):
    total_count = graphene.IntField()

    def resolve_total_count(self, args, info):
        return len(self.get_connection_data())


class Show(DjangoNode):
    class Meta:
        model = Show
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Review(DjangoNode):
    class Meta:
        model = Review
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class User(DjangoNode):
    class Meta:
        model = User
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Group(DjangoNode):
    class Meta:
        model = Group
        exclude_fields = ('created', 'edited')

    connection_type = Connection

class Query(graphene.ObjectType):
    all_shows = DjangoConnectionField(Show)
    all_reviews = DjangoConnectionField(Review)
    all_users = DjangoConnectionField(User)
    all_groups = DjangoConnectionField(Group)
    show = relay.NodeField(Show)
    review = relay.NodeField(Review)
    user = relay.NodeField(User)
    group = relay.NodeField(Group)
    node = relay.NodeField()
    viewer = graphene.Field('self')

    @resolve_only_args
    def resolve_all_shows(self, **kwargs):
        return Show.objects.all()

    @resolve_only_args
    def resolve_all_reviews(self, **kwargs):
        return Review.objects.all()

    @resolve_only_args
    def resolve_all_users(self, **kwargs):
        return User.objects.all()

    @resolve_only_args
    def resolve_all_groups(self, **kwargs):
        return Group.objects.all()

    def resolve_viewer(self, *args, **kwargs):
        return self


schema.query = Query
