from django.db import models


# Author Model
# This model represents an author who can write multiple books.
# It establishes the "one" side of a one-to-many relationship with the Book model.
class Author(models.Model):
    """
    Author model to store information about book authors.
    
    Fields:
        name: The full name of the author (max 200 characters)
    
    Relationships:
        - One Author can have many Books (one-to-many relationship)
        - Related books can be accessed via the 'books' reverse relationship
    """
    name = models.CharField(max_length=200, help_text="Full name of the author")
    
    def __str__(self):
        """String representation of the Author model"""
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


# Book Model
# This model represents a book and establishes a many-to-one relationship with Author.
# Each book must be associated with exactly one author.
class Book(models.Model):
    """
    Book model to store information about books.
    
    Fields:
        title: The title of the book (max 200 characters)
        publication_year: The year the book was published (integer)
        author: Foreign key relationship to the Author model
    
    Relationships:
        - Many Books can belong to one Author (many-to-one relationship)
        - The 'author' field creates a foreign key constraint
        - When an author is deleted, all their books are also deleted (CASCADE)
        - The related_name='books' allows reverse lookup from Author to Books
    """
    title = models.CharField(max_length=200, help_text="Title of the book")
    publication_year = models.IntegerField(help_text="Year the book was published")
    
    # Foreign Key Relationship
    # - on_delete=models.CASCADE: When an author is deleted, delete all their books
    # - related_name='books': Allows accessing an author's books via author.books.all()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        """String representation of the Book model"""
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
    
    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
