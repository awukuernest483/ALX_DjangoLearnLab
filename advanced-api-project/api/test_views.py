from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from datetime import datetime


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for the Book API endpoints.
    
    This test class covers:
    - CRUD operations (Create, Read, Update, Delete)
    - Filtering functionality
    - Searching functionality
    - Ordering functionality
    - Permission and authentication checks
    """
    
    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        
        This method runs before each test to ensure a clean state.
        Creates:
        - Test users (authenticated and unauthenticated)
        - Sample authors
        - Sample books with different publication years
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='Jane Austen')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author3
        )
        
        # Set up API client
        self.client = APIClient()
    
    # ========== CRUD Operation Tests ==========
    
    def test_get_all_books(self):
        """
        Test retrieving a list of all books.
        
        Verifies:
        - Endpoint returns 200 OK status
        - All books are returned in the response
        - No authentication is required (public access)
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_get_single_book(self):
        """
        Test retrieving a single book by ID.
        
        Verifies:
        - Endpoint returns 200 OK status
        - Correct book data is returned
        - No authentication is required
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter and the Philosopher\'s Stone')
        self.assertEqual(response.data['publication_year'], 1997)
    
    def test_create_book_authenticated(self):
        """
        Test creating a new book as an authenticated user.
        
        Verifies:
        - Authenticated users can create books
        - Endpoint returns 201 CREATED status
        - Book is actually created in the database
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(title='New Book').publication_year, 2020)
    
    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books.
        
        Verifies:
        - Endpoint returns 401 UNAUTHORIZED or 403 FORBIDDEN
        - No book is created in the database
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.pk
        }
        response = self.client.post(url, data)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 3)  # No new book created
    
    def test_update_book_authenticated(self):
        """
        Test updating a book as an authenticated user.
        
        Verifies:
        - Authenticated users can update books
        - Endpoint returns 200 OK status
        - Book data is actually updated in the database
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Updated Title',
            'publication_year': 1998,
            'author': self.author1.pk
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
        self.assertEqual(self.book1.publication_year, 1998)
    
    def test_update_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books.
        
        Verifies:
        - Endpoint returns 401 UNAUTHORIZED or 403 FORBIDDEN
        - Book data is not modified
        """
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1998,
            'author': self.author1.pk
        }
        response = self.client.put(url, data)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone')
    
    def test_partial_update_book(self):
        """
        Test partial update (PATCH) of a book.
        
        Verifies:
        - Authenticated users can partially update books
        - Only specified fields are updated
        - Other fields remain unchanged
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)  # Unchanged
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book as an authenticated user.
        
        Verifies:
        - Authenticated users can delete books
        - Endpoint returns 204 NO CONTENT status
        - Book is actually removed from the database
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())
    
    def test_delete_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books.
        
        Verifies:
        - Endpoint returns 401 UNAUTHORIZED or 403 FORBIDDEN
        - Book is not deleted from the database
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Book.objects.count(), 3)  # Book still exists
    
    # ========== Validation Tests ==========
    
    def test_create_book_future_year_validation(self):
        """
        Test custom validation for publication_year.
        
        Verifies:
        - Books with future publication years are rejected
        - Endpoint returns 400 BAD REQUEST status
        - Appropriate error message is returned
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        future_year = datetime.now().year + 10
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_current_year(self):
        """
        Test that books with current year are accepted.
        
        Verifies:
        - Books with the current year pass validation
        - Endpoint returns 201 CREATED status
        """
        self.client.force_authenticate(user=self.user)
        
        url = reverse('book-create')
        current_year = datetime.now().year
        data = {
            'title': 'Current Year Book',
            'publication_year': current_year,
            'author': self.author1.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # ========== Filtering Tests ==========
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by exact title.
        
        Verifies:
        - Filtering by title returns only matching books
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': '1984'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID.
        
        Verifies:
        - Filtering by author returns only books by that author
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.pk)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Verifies:
        - Filtering by year returns only books from that year
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    # ========== Searching Tests ==========
    
    def test_search_books_by_title(self):
        """
        Test searching books by title keyword.
        
        Verifies:
        - Search finds books with matching title text
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Potter'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Potter', response.data[0]['title'])
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        
        Verifies:
        - Search finds books by authors with matching names
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
    
    def test_search_case_insensitive(self):
        """
        Test that search is case-insensitive.
        
        Verifies:
        - Search works regardless of case
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'pride'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    # ========== Ordering Tests ==========
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        
        Verifies:
        - Books are returned in alphabetical order by title
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        
        Verifies:
        - Books are returned in reverse alphabetical order by title
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_books_by_publication_year_ascending(self):
        """
        Test ordering books by publication year in ascending order.
        
        Verifies:
        - Books are returned from oldest to newest
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        
        Verifies:
        - Books are returned from newest to oldest
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_default_ordering(self):
        """
        Test that default ordering is by publication year descending.
        
        Verifies:
        - Without explicit ordering, books are ordered by newest first
        - Endpoint returns 200 OK status
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


class AuthorAPITestCase(APITestCase):
    """
    Test suite for Author API endpoints with nested serialization.
    
    This test class verifies:
    - Nested serialization of books within author data
    - Author list and detail endpoints
    """
    
    def setUp(self):
        """Set up test data for author tests."""
        self.author = Author.objects.create(name='Test Author')
        self.book1 = Book.objects.create(
            title='Book 1',
            publication_year=2020,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Book 2',
            publication_year=2021,
            author=self.author
        )
        self.client = APIClient()
    
    def test_get_author_with_nested_books(self):
        """
        Test retrieving an author with nested book data.
        
        Verifies:
        - Author data includes nested books array
        - All books by the author are included
        - Nested books contain correct data
        """
        url = reverse('author-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
        self.assertEqual(len(response.data['books']), 2)
        self.assertIn('title', response.data['books'][0])
        self.assertIn('publication_year', response.data['books'][0])
    
    def test_get_all_authors_with_books(self):
        """
        Test retrieving all authors with nested book data.
        
        Verifies:
        - All authors are returned
        - Each author includes their books
        """
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn('books', response.data[0])
