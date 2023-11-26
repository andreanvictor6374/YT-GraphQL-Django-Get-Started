from django.urls import path
from graphene_django.views import GraphQLView
from spyne.server.django import DjangoApplication
from .soap_services import application as book_soap_application
from books.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Only a single URL to access GraphQL
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('soap/books/', csrf_exempt(DjangoApplication(book_soap_application))),

]
