from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # ListAPIView endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Include all CRUD routes from the router
    path('', include(router.urls)),
]
