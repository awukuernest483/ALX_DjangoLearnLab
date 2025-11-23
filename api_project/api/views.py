from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides standard CRUD actions for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
