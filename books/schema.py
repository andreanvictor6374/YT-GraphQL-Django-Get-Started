import graphene
from graphene_django import DjangoObjectType
from .models import Books

class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")

class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType, title=graphene.String(required=False))

    def resolve_all_books(root, info, title=None):
        if title:
            return Books.objects.filter(title__icontains=title)
        return Books.objects.all()

schema = graphene.Schema(query=Query)
