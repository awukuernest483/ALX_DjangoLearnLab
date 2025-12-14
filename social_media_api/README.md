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

---

## User Authentication

The API uses Token Authentication provided by Django REST Framework.

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login and get token |
| GET | `/api/profile/` | Get current user profile |
| PUT | `/api/profile/` | Update current user profile |
| GET | `/api/users/` | List all users |

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

## Follow System

Users can follow and unfollow other users to build their social network.

### Follow Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/follow/<user_id>/` | Follow a user |
| POST | `/api/unfollow/<user_id>/` | Unfollow a user |

#### Follow a User
```bash
curl -X POST http://127.0.0.1:8000/api/follow/2/ \
  -H "Authorization: Token <your_token>"
```
Response:
```json
{"message": "You are now following username."}
```

#### Unfollow a User
```bash
curl -X POST http://127.0.0.1:8000/api/unfollow/2/ \
  -H "Authorization: Token <your_token>"
```
Response:
```json
{"message": "You have unfollowed username."}
```

#### Error Cases
- **Following yourself**: Returns 400 Bad Request
- **Already following**: Returns 200 with message "You are already following..."
- **Not following**: Returns 200 with message "You are not following..."
- **User not found**: Returns 404 Not Found

---

## Feed

Get a personalized feed of posts from users you follow.

### Feed Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed/` | Get posts from followed users |

#### Get Feed
```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/feed/
```
Response:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "author": "followed_user",
      "title": "Latest Post",
      "content": "This is the newest post from someone you follow.",
      "created_at": "2025-12-14T15:00:00Z",
      "updated_at": "2025-12-14T15:00:00Z",
      "comments": []
    }
  ]
}
```

**Note**: Posts are ordered by creation date (most recent first).

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
- **Follow/Unfollow**: Requires authentication, users can only modify their own following list
- **Feed**: Requires authentication

---

## Models

### User Model
The custom user model extends `AbstractUser` and includes:
- `bio`: Text field for user biography
- `profile_picture`: Image field for profile pictures
- `followers`: ManyToMany field referencing self (symmetrical=False)
  - Access followers: `user.followers.all()`
  - Access following: `user.following.all()`

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

---

## API Summary

| Category | Endpoint | Method | Auth Required |
|----------|----------|--------|---------------|
| Auth | `/api/register/` | POST | No |
| Auth | `/api/login/` | POST | No |
| Auth | `/api/profile/` | GET, PUT | Yes |
| Users | `/api/users/` | GET | Yes |
| Follow | `/api/follow/<user_id>/` | POST | Yes |
| Follow | `/api/unfollow/<user_id>/` | POST | Yes |
| Feed | `/api/feed/` | GET | Yes |
| Posts | `/api/posts/` | GET, POST | POST only |
| Posts | `/api/posts/<id>/` | GET, PUT, DELETE | PUT/DELETE only |
| Comments | `/api/comments/` | GET, POST | POST only |
| Comments | `/api/comments/<id>/` | GET, PUT, DELETE | PUT/DELETE only |
