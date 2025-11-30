from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# BookSerializer
# This serializer handles the serialization of Book model instances.
# It includes custom validation to ensure data integrity.
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles all fields of the Book model and includes
    custom validation to ensure the publication_year is not in the future.
    
    Fields:
        - id: Auto-generated primary key
        - title: The title of the book
        - publication_year: The year the book was published
        - author: Foreign key reference to the Author (ID)
    
    Custom Validation:
        - publication_year: Must not be greater than the current year
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation method for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering invalid publication dates.
        
        Args:
            value: The publication_year value to validate
            
        Returns:
            The validated publication_year value
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        return value


# AuthorSerializer
# This serializer handles the serialization of Author model instances
# and includes nested serialization of related Book instances.
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates nested relationships in Django REST Framework.
    It includes the author's name and dynamically serializes all books written
    by the author using the BookSerializer.
    
    Fields:
        - id: Auto-generated primary key
        - name: The name of the author
        - books: Nested serialization of all related Book instances
    
    Nested Relationship Handling:
        - The 'books' field uses the reverse relationship defined in the Book model
          (related_name='books' in the ForeignKey)
        - many=True indicates that this is a one-to-many relationship
        - read_only=True prevents creating/updating books through the author endpoint
        - The BookSerializer is used to serialize each related book
    
    How it works:
        1. When an Author instance is serialized, Django REST Framework automatically
           queries all related Book instances using the 'books' reverse relationship
        2. Each Book instance is then serialized using the BookSerializer
        3. The result is a nested JSON structure with the author's information
           and an array of their books
    
    Example JSON output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    """
    
    # Nested serialization of related books
    # - The field name 'books' matches the related_name in the Book model's ForeignKey
    # - many=True indicates this is a one-to-many relationship (one author, many books)
    # - read_only=True makes this field read-only (books cannot be created/updated via this endpoint)
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
