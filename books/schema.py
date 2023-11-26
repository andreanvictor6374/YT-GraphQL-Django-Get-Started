import graphene
from graphene_django import DjangoObjectType
from .models import Books, Order, Customer


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email')


class OrderType(DjangoObjectType):
    customer = graphene.Field(CustomerType)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'book', 'quantity')


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType, title=graphene.String(required=False))
    book = graphene.Field(BooksType, id=graphene.Int(required=True))
    books = graphene.List(BooksType, search=graphene.String(required=False))

    order = graphene.Field(OrderType, id=graphene.Int(required=True))


    def resolve_all_books(root, info, title=None):
        if title:
            return Books.objects.filter(title__icontains=title)
        return Books.objects.all()

    def resolve_book(root, info, id):
        return Books.objects.get(id=id)

    def resolve_books(root, info, search=None):
        if search:
            return Books.objects.filter(Q(title__icontains=search) | Q(excerpt__icontains=search))
        return Books.objects.all()
    def resolve_order(self, info, id):
        return Order.objects.get(pk=id)

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        excerpt = graphene.String(required=True)

    # The response fields
    book = graphene.Field(BooksType)

    @staticmethod
    def mutate(root, info, title, excerpt):
        book = Books(title=title, excerpt=excerpt)
        book.save()
        # Return an instance of this mutation
        return CreateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        try:
            book = Books.objects.get(pk=id)
            book.delete()
            return DeleteBook(ok=True)
        except Books.DoesNotExist:
            return DeleteBook(ok=False)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        excerpt = graphene.String()

    # The response fields
    book = graphene.Field(BooksType)

    @staticmethod
    def mutate(root, info, id, title=None, excerpt=None):
        book = Books.objects.get(pk=id)
        if title is not None:
            book.title = title
        if excerpt is not None:
            book.excerpt = excerpt
        book.save()
        return UpdateBook(book=book)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.Int(required=True)
        book_id = graphene.Int(required=True)
        quantity = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, customer_id, book_id, quantity):
        # You may need to add error handling here
        order = Order(
            customer_id=customer_id,
            book_id=book_id,
            quantity=quantity
        )
        order.save()
        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    delete_book = DeleteBook.Field()
    update_book = UpdateBook.Field()
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
