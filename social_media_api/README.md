# Social Media API

## Project Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Install Dependencies**:
   Ensure you have a virtual environment set up.
   ```bash
   pip install django djangorestframework pillow django-filter
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

## User Authentication

The API uses Token Authentication provided by Django REST Framework.

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login and get token |
| GET | `/api/profile/` | Get current user profile |
| PUT | `/api/profile/` | Update current user profile |

#### Register
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -d "username=newuser&password=yourpassword&email=user@example.com&bio=Hello"
```
Response:
```json
{"token": "your_auth_token_here"}
```

#### Login
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -d "username=newuser&password=yourpassword"
```
Response:
```json
{"token": "your_auth_token_here"}
```

#### Get Profile
```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/profile/
```

---

## Posts API

### Post Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List all posts (paginated) |
| POST | `/api/posts/` | Create a new post |
| GET | `/api/posts/{id}/` | Retrieve a specific post |
| PUT | `/api/posts/{id}/` | Update a post (author only) |
| DELETE | `/api/posts/{id}/` | Delete a post (author only) |

#### List Posts
```bash
curl http://127.0.0.1:8000/api/posts/
```
Response:
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "username",
      "title": "My First Post",
      "content": "Hello World!",
      "created_at": "2025-12-14T12:00:00Z",
      "updated_at": "2025-12-14T12:00:00Z",
      "comments": []
    }
  ]
}
```

#### Create Post (requires authentication)
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <your_token>" \
  -d "title=My Post&content=This is my post content"
```

#### Search Posts by Title or Content
```bash
curl "http://127.0.0.1:8000/api/posts/?search=keyword"
```

#### Filter Posts by Author
```bash
curl "http://127.0.0.1:8000/api/posts/?author=1"
```

---

## Comments API

### Comment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/comments/` | List all comments (paginated) |
| POST | `/api/comments/` | Create a new comment |
| GET | `/api/comments/{id}/` | Retrieve a specific comment |
| PUT | `/api/comments/{id}/` | Update a comment (author only) |
| DELETE | `/api/comments/{id}/` | Delete a comment (author only) |

#### Create Comment (requires authentication)
```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token <your_token>" \
  -d "post=1&content=Great post!"
```

#### Filter Comments by Post
```bash
curl "http://127.0.0.1:8000/api/comments/?post=1"
```

---

## Pagination

All list endpoints support pagination:
- Default page size: 10 items
- Query parameters:
  - `page`: Page number (e.g., `?page=2`)
  - `page_size`: Items per page (e.g., `?page_size=20`)

---

## Filtering and Search

### Posts
- **Search**: `?search=<keyword>` - Searches in title and content
- **Filter by author**: `?author=<user_id>`
- **Ordering**: `?ordering=created_at` or `?ordering=-created_at` (descending)

### Comments
- **Filter by post**: `?post=<post_id>`
- **Filter by author**: `?author=<user_id>`
- **Ordering**: `?ordering=created_at`

---

## Permissions

- **Read operations**: Open to all users (authenticated or not)
- **Create operations**: Require authentication
- **Update/Delete operations**: Only the author can modify their own posts/comments

---

## Models

### User Model
The custom user model extends `AbstractUser` and includes:
- `bio`: Text field for user biography
- `profile_picture`: Image field for profile pictures
- `followers`: ManyToMany field referencing self (symmetrical=False)

### Post Model
- `author`: ForeignKey to User
- `title`: CharField (max 255 characters)
- `content`: TextField
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

### Comment Model
- `post`: ForeignKey to Post
- `author`: ForeignKey to User
- `content`: TextField
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)
