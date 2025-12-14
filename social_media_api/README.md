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
   pip install django djangorestframework pillow
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

### Endpoints

*   **Register**: `POST /api/register/`
    *   Body: `{"username": "...", "password": "...", "email": "...", "bio": "...", "profile_picture": "..."}`
    *   Returns: Auth Token.

*   **Login**: `POST /api/login/`
    *   Body: `{"username": "...", "password": "..."}`
    *   Returns: Auth Token.

*   **Profile**: `GET /api/profile/`
    *   Headers: `Authorization: Token <your_token>`
    *   Returns: Current user profile.

## User Model

The custom user model extends `AbstractUser` and includes:
*   `bio`: Text field for user biography.
*   `profile_picture`: Image field.
*   `followers`: ManyToMany field referencing `self` (symmetrical=False).
