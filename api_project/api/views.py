from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Simple list view (read-only)
class BookList(generics.ListAPIView):
    """
    A simple view to list all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Full CRUD viewset
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD actions for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
