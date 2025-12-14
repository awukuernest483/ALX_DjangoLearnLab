# Social Media API

A Django REST Framework-based social media API with user authentication, posts, comments, likes, follows, feed, and notifications.

## Project Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Install Dependencies**:
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

**Note**: Following a user creates a notification for the followed user.

---

## Feed

Get a personalized feed of posts from users you follow.

### Feed Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed/` | Get posts from followed users |

```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/feed/
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

#### Create Post
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <your_token>" \
  -d "title=My Post&content=This is my post content"
```

#### Search Posts
```bash
curl "http://127.0.0.1:8000/api/posts/?search=keyword"
```

---

## Likes API

Users can like and unlike posts. Liking a post creates a notification for the post author.

### Like Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/posts/<id>/like/` | Like a post |
| POST | `/api/posts/<id>/unlike/` | Unlike a post |

#### Like a Post
```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
  -H "Authorization: Token <your_token>"
```
Response:
```json
{"message": "Post liked successfully."}
```

#### Unlike a Post
```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/unlike/ \
  -H "Authorization: Token <your_token>"
```
Response:
```json
{"message": "Post unliked successfully."}
```

#### Error Cases
- **Already liked**: Returns 200 with message "You have already liked this post."
- **Not liked**: Returns 400 with message "You have not liked this post."

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

**Note**: Creating a comment creates a notification for the post author.

```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token <your_token>" \
  -d "post=1&content=Great post!"
```

---

## Notifications API

Users receive notifications for various interactions:
- When someone follows them
- When someone likes their post
- When someone comments on their post

### Notification Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | Get all notifications for the user |

#### Get Notifications
```bash
curl -H "Authorization: Token <your_token>" http://127.0.0.1:8000/api/notifications/
```
Response:
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "recipient": 1,
      "actor": "username",
      "verb": "liked your post",
      "target_type": "post",
      "target_id": 1,
      "timestamp": "2025-12-14T12:00:00Z",
      "read": false
    }
  ]
}
```

**Note**: Unread notifications are shown first.

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
- **Ordering**: `?ordering=created_at` or `?ordering=-created_at`

### Comments
- **Filter by post**: `?post=<post_id>`
- **Filter by author**: `?author=<user_id>`

---

## Permissions

| Operation | Permission |
|-----------|------------|
| Read posts/comments | Public |
| Create posts/comments | Authenticated |
| Update/Delete posts/comments | Author only |
| Like/Unlike posts | Authenticated |
| Follow/Unfollow users | Authenticated |
| View feed | Authenticated |
| View notifications | Authenticated (own only) |

---

## Models

### User Model (CustomUser)
- `username`, `email`, `password` (inherited from AbstractUser)
- `bio`: Text field for user biography
- `profile_picture`: Image field for profile pictures
- `followers`: ManyToMany field (symmetrical=False)

### Post Model
- `author`: ForeignKey to User
- `title`: CharField (max 255)
- `content`: TextField
- `created_at`, `updated_at`: DateTimeField

### Comment Model
- `post`: ForeignKey to Post
- `author`: ForeignKey to User
- `content`: TextField
- `created_at`, `updated_at`: DateTimeField

### Like Model
- `user`: ForeignKey to User
- `post`: ForeignKey to Post
- `created_at`: DateTimeField
- Unique constraint on (user, post)

### Notification Model
- `recipient`: ForeignKey to User (who receives)
- `actor`: ForeignKey to User (who performed action)
- `verb`: CharField (action description)
- `target`: GenericForeignKey (target object)
- `timestamp`: DateTimeField
- `read`: BooleanField

---

## API Summary

| Category | Endpoint | Method | Auth |
|----------|----------|--------|------|
| Auth | `/api/register/` | POST | No |
| Auth | `/api/login/` | POST | No |
| Auth | `/api/profile/` | GET, PUT | Yes |
| Users | `/api/users/` | GET | Yes |
| Follow | `/api/follow/<user_id>/` | POST | Yes |
| Follow | `/api/unfollow/<user_id>/` | POST | Yes |
| Feed | `/api/feed/` | GET | Yes |
| Posts | `/api/posts/` | GET, POST | POST: Yes |
| Posts | `/api/posts/<id>/` | GET, PUT, DELETE | PUT/DELETE: Yes |
| Likes | `/api/posts/<id>/like/` | POST | Yes |
| Likes | `/api/posts/<id>/unlike/` | POST | Yes |
| Comments | `/api/comments/` | GET, POST | POST: Yes |
| Comments | `/api/comments/<id>/` | GET, PUT, DELETE | PUT/DELETE: Yes |
| Notifications | `/api/notifications/` | GET | Yes |
