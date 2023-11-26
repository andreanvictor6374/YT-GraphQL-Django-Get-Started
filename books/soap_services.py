from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11

from .models import Books


class BookService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def list_books(ctx, title_filter=None):
        """
        Returns a list of book titles, optionally filtered by a title.
        """
        books = Books.objects.all()
        if title_filter:
            books = books.filter(title__icontains=title_filter)
        return (book.title for book in books)

    @rpc(Integer, _returns=Unicode)
    def get_book_excerpt(ctx, book_id):
        """
        Returns the excerpt of a book given its ID.
        """
        try:
            return Books.objects.get(id=book_id).excerpt
        except Books.DoesNotExist:
            return "Book not found"


# Django application
application = Application([BookService],
                          tns='your.namespace.here',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
