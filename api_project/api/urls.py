from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create DRF router and register BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Simple read-only list endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Include all CRUD endpoints from the router
    path('', include(router.urls)),
]
