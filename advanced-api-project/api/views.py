from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django_filters import rest_framework
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


# Book List View
# Provides a read-only list of all books with filtering, searching, and ordering capabilities
class BookListView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of all books.
    
    This view provides:
    - Public read access (no authentication required)
    - Filtering by title, author, and publication_year
    - Text search on title and author name
    - Ordering by title and publication_year
    
    Permissions:
        - AllowAny: Anyone can access this endpoint (read-only)
    
    Filtering:
        - Filter by exact title: ?title=Book Title
        - Filter by author ID: ?author=1
        - Filter by publication year: ?publication_year=2020
    
    Searching:
        - Search in title and author name: ?search=keyword
    
    Ordering:
        - Order by title ascending: ?ordering=title
        - Order by title descending: ?ordering=-title
        - Order by publication year: ?ordering=publication_year
        - Order by publication year descending: ?ordering=-publication_year
    
    Example URLs:
        - /books/ - Get all books
        - /books/?title=Django - Filter by title
        - /books/?search=python - Search for "python" in title or author
        - /books/?ordering=-publication_year - Order by newest first
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public read access
    
    # Configure filtering, searching, and ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering: Allow filtering by these exact field values
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Searching: Allow text search in these fields
    search_fields = ['title', 'author__name']
    
    # Ordering: Allow ordering by these fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['-publication_year']  # Default ordering


# Book Detail View
# Provides read-only access to a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single book by ID.
    
    This view provides:
    - Public read access to individual book details
    - No authentication required
    
    Permissions:
        - AllowAny: Anyone can access this endpoint (read-only)
    
    Example URL:
        - /books/1/ - Get book with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Public read access


# Book Create View
# Allows authenticated users to create new books
class BookCreateView(generics.CreateAPIView):
    """
    API endpoint for creating a new book.
    
    This view provides:
    - Book creation functionality
    - Automatic validation using BookSerializer
    - Custom validation for publication_year (not in future)
    
    Permissions:
        - IsAuthenticated: Only authenticated users can create books
    
    Request Body (JSON):
        {
            "title": "Book Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Example URL:
        - POST /books/create/ - Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create


# Book Update View
# Allows authenticated users to update existing books
class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint for updating an existing book.
    
    This view provides:
    - Full update (PUT) and partial update (PATCH) functionality
    - Automatic validation using BookSerializer
    - Custom validation for publication_year (not in future)
    
    Permissions:
        - IsAuthenticated: Only authenticated users can update books
    
    Request Body (JSON) for full update (PUT):
        {
            "title": "Updated Book Title",
            "publication_year": 2023,
            "author": 1
        }
    
    Request Body (JSON) for partial update (PATCH):
        {
            "title": "Updated Book Title"
        }
    
    Example URLs:
        - PUT /books/1/update/ - Full update of book with ID 1
        - PATCH /books/1/update/ - Partial update of book with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update


# Book Delete View
# Allows authenticated users to delete books
class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint for deleting a book.
    
    This view provides:
    - Book deletion functionality
    - Permanent removal from database
    
    Permissions:
        - IsAuthenticated: Only authenticated users can delete books
    
    Example URL:
        - DELETE /books/1/delete/ - Delete book with ID 1
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete


# Author List View
# Provides a read-only list of all authors with their books (nested)
class AuthorListView(generics.ListAPIView):
    """
    API endpoint for retrieving a list of all authors with their books.
    
    This view demonstrates nested serialization:
    - Each author includes a nested list of their books
    - Uses AuthorSerializer which includes BookSerializer
    
    Permissions:
        - AllowAny: Anyone can access this endpoint (read-only)
    
    Example URL:
        - /authors/ - Get all authors with their books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


# Author Detail View
# Provides read-only access to a single author with their books
class AuthorDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single author with their books.
    
    This view demonstrates nested serialization for a single instance:
    - Returns author details with nested list of their books
    - Uses AuthorSerializer which includes BookSerializer
    
    Permissions:
        - AllowAny: Anyone can access this endpoint (read-only)
    
    Example URL:
        - /authors/1/ - Get author with ID 1 and their books
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
