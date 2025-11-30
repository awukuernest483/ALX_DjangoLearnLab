from django.contrib import admin
from .models import Author, Book


# Register Author model with admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration for Author model"""
    list_display = ['name']
    search_fields = ['name']


# Register Book model with admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model"""
    list_display = ['title', 'author', 'publication_year']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering = ['-publication_year']
