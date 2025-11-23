from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    A simple view to list all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
