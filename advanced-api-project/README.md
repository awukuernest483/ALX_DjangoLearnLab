# Advanced Django REST Framework API Project

A comprehensive Django REST Framework API project demonstrating advanced features including custom serializers with nested relationships, generic views, filtering, searching, ordering, and comprehensive testing.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Serializers](#serializers)
- [Advanced Features](#advanced-features)
- [Authentication & Permissions](#authentication--permissions)
- [Testing](#testing)
- [Usage Examples](#usage-examples)

## Features

✅ **Custom Serializers** with nested relationships  
✅ **Generic Views** for CRUD operations  
✅ **Filtering** by multiple fields  
✅ **Text Search** across related models  
✅ **Ordering** with customizable sort options  
✅ **Permission-based Access Control**  
✅ **Comprehensive Unit Tests** (24 test cases)  
✅ **Custom Validation** for data integrity  

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Steps

1. **Clone the repository:**
   ```bash
   cd /Users/eawuku/Documents/GitHub/ALX_DjangoLearnLab/advanced-api-project
   ```

2. **Activate virtual environment:**
   ```bash
   source ../venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework django-filter
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Book Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/books/` | List all books | No |
| GET | `/api/books/<id>/` | Get single book | No |
| POST | `/api/books/create/` | Create new book | Yes |
| PUT/PATCH | `/api/books/<id>/update/` | Update book | Yes |
| DELETE | `/api/books/<id>/delete/` | Delete book | Yes |

### Author Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/authors/` | List all authors with books | No |
| GET | `/api/authors/<id>/` | Get single author with books | No |

## Models

### Author Model

Represents a book author.

**Fields:**
- `id`: Auto-generated primary key
- `name`: CharField (max 200 characters) - Author's full name

**Relationships:**
- One-to-many with Book model (one author can have many books)

### Book Model

Represents a book with publication information.

**Fields:**
- `id`: Auto-generated primary key
- `title`: CharField (max 200 characters) - Book title
- `publication_year`: IntegerField - Year of publication
- `author`: ForeignKey to Author - The book's author

**Relationships:**
- Many-to-one with Author model (many books belong to one author)
- CASCADE deletion (when author is deleted, their books are also deleted)

## Serializers

### BookSerializer

Serializes all fields of the Book model with custom validation.

**Custom Validation:**
- `publication_year`: Must not be in the future
- Returns appropriate error message if validation fails

**Example JSON:**
```json
{
  "id": 1,
  "title": "Harry Potter and the Philosopher's Stone",
  "publication_year": 1997,
  "author": 1
}
```

### AuthorSerializer

Serializes Author model with nested Book serialization.

**Features:**
- Includes all author fields
- Dynamically serializes related books using BookSerializer
- Demonstrates one-to-many relationship handling

**Example JSON:**
```json
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
```

## Advanced Features

### Filtering

Filter books by exact field values using query parameters:

```bash
# Filter by title
GET /api/books/?title=1984

# Filter by author ID
GET /api/books/?author=1

# Filter by publication year
GET /api/books/?publication_year=1997

# Combine multiple filters
GET /api/books/?author=1&publication_year=1997
```

### Searching

Perform text search across title and author name:

```bash
# Search in title and author name
GET /api/books/?search=Potter

# Search is case-insensitive
GET /api/books/?search=orwell
```

### Ordering

Sort results by any allowed field:

```bash
# Order by title (ascending)
GET /api/books/?ordering=title

# Order by title (descending)
GET /api/books/?ordering=-title

# Order by publication year (ascending)
GET /api/books/?ordering=publication_year

# Order by publication year (descending)
GET /api/books/?ordering=-publication_year
```

**Default Ordering:** Books are ordered by publication year (newest first) by default.

### Combining Features

You can combine filtering, searching, and ordering:

```bash
# Search for "Harry" and order by publication year
GET /api/books/?search=Harry&ordering=publication_year

# Filter by author and order by title
GET /api/books/?author=1&ordering=title
```

## Authentication & Permissions

### Public Endpoints (No Authentication Required)

- `GET /api/books/` - List all books
- `GET /api/books/<id>/` - Get single book
- `GET /api/authors/` - List all authors
- `GET /api/authors/<id>/` - Get single author

### Protected Endpoints (Authentication Required)

- `POST /api/books/create/` - Create book
- `PUT/PATCH /api/books/<id>/update/` - Update book
- `DELETE /api/books/<id>/delete/` - Delete book

### Authentication Methods

The API supports Django REST Framework's default authentication:
- Session Authentication (for browsable API)
- Token Authentication (can be configured)
- Basic Authentication (for testing)

## Testing

### Running Tests

Run the complete test suite:

```bash
python manage.py test api
```

Run specific test class:

```bash
python manage.py test api.test_views.BookAPITestCase
```

Run specific test method:

```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Test Coverage

The test suite includes **24 comprehensive tests** covering:

#### CRUD Operations (11 tests)
- ✅ List all books
- ✅ Retrieve single book
- ✅ Create book (authenticated)
- ✅ Create book (unauthenticated - should fail)
- ✅ Update book (authenticated)
- ✅ Update book (unauthenticated - should fail)
- ✅ Partial update book
- ✅ Delete book (authenticated)
- ✅ Delete book (unauthenticated - should fail)
- ✅ Get author with nested books
- ✅ Get all authors with books

#### Validation (2 tests)
- ✅ Reject future publication year
- ✅ Accept current year

#### Filtering (3 tests)
- ✅ Filter by title
- ✅ Filter by author
- ✅ Filter by publication year

#### Searching (3 tests)
- ✅ Search by title
- ✅ Search by author name
- ✅ Case-insensitive search

#### Ordering (5 tests)
- ✅ Order by title (ascending)
- ✅ Order by title (descending)
- ✅ Order by publication year (ascending)
- ✅ Order by publication year (descending)
- ✅ Default ordering

## Usage Examples

### Using cURL

#### List all books
```bash
curl http://localhost:8000/api/books/
```

#### Get a specific book
```bash
curl http://localhost:8000/api/books/1/
```

#### Create a book (requires authentication)
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
  }'
```

#### Update a book
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "Updated Title",
    "publication_year": 2023,
    "author": 1
  }'
```

#### Partial update
```bash
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title": "New Title Only"}'
```

#### Delete a book
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -u username:password
```

#### Search and filter
```bash
# Search for books
curl "http://localhost:8000/api/books/?search=Potter"

# Filter by author
curl "http://localhost:8000/api/books/?author=1"

# Order by publication year
curl "http://localhost:8000/api/books/?ordering=-publication_year"

# Combine features
curl "http://localhost:8000/api/books/?search=Harry&ordering=publication_year"
```

### Using Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# List all books
response = requests.get(f"{BASE_URL}/books/")
books = response.json()

# Get a specific book
response = requests.get(f"{BASE_URL}/books/1/")
book = response.json()

# Create a book (with authentication)
auth = ('username', 'password')
data = {
    "title": "New Book",
    "publication_year": 2023,
    "author": 1
}
response = requests.post(f"{BASE_URL}/books/create/", json=data, auth=auth)

# Search books
response = requests.get(f"{BASE_URL}/books/", params={"search": "Potter"})
results = response.json()

# Filter and order
params = {
    "author": 1,
    "ordering": "-publication_year"
}
response = requests.get(f"{BASE_URL}/books/", params=params)
filtered_books = response.json()
```

### Using Django Shell

```python
python manage.py shell

# Import models
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
author = Author.objects.create(name="J.K. Rowling")

# Create books
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author
)

# Serialize a book
serializer = BookSerializer(book1)
print(serializer.data)

# Serialize an author with nested books
author_serializer = AuthorSerializer(author)
print(author_serializer.data)
```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py          # Admin configuration
│   ├── models.py         # Author and Book models
│   ├── serializers.py    # BookSerializer and AuthorSerializer
│   ├── views.py          # Generic views for CRUD operations
│   ├── urls.py           # API URL patterns
│   ├── test_views.py     # Comprehensive test suite
│   └── migrations/
├── manage.py
└── db.sqlite3
```

## Key Implementation Details

### Model Relationships

The project demonstrates a **one-to-many relationship**:
- One Author can have many Books
- Each Book belongs to exactly one Author
- When an Author is deleted, all their Books are also deleted (CASCADE)
- The `related_name='books'` allows reverse lookup: `author.books.all()`

### Nested Serialization

The `AuthorSerializer` demonstrates nested serialization:
- Uses `BookSerializer(many=True, read_only=True)` for the books field
- Automatically queries and serializes all related books
- Returns a nested JSON structure with author and their books

### Custom Validation

The `BookSerializer` includes custom validation:
- `validate_publication_year()` method ensures the year is not in the future
- Compares against the current year using `datetime.now().year`
- Raises `serializers.ValidationError` with a descriptive message

### Generic Views

The project uses DRF's generic views for clean, reusable code:
- `ListAPIView` - Read-only list endpoint
- `RetrieveAPIView` - Read-only detail endpoint
- `CreateAPIView` - Create-only endpoint
- `UpdateAPIView` - Update-only endpoint (PUT/PATCH)
- `DestroyAPIView` - Delete-only endpoint

## Contributing

This project was created as a learning exercise for advanced Django REST Framework features. Feel free to use it as a reference or starting point for your own projects.

## License

This project is part of the ALX Django Learn Lab curriculum.
