import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField

from .models import User, Show, Review


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


class Query(graphene.ObjectType):
    all_shows = DjangoConnectionField(Show)
    all_reviews = DjangoConnectionField(Review)
    show = relay.NodeField(Show)
    review = relay.NodeField(Review)
    node = relay.NodeField()
    viewer = graphene.Field('self')

    @resolve_only_args
    def resolve_all_shows(self, **kwargs):
        return Show.objects.all()

    @resolve_only_args
    def resolve_all_reviews(self, **kwargs):
        return Review.objects.all()

    def resolve_viewer(self, *args, **kwargs):
        return self


schema.query = Query
