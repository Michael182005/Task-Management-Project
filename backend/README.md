# Task Management Backend

FastAPI backend for a task management system with JWT authentication, role-based access, and PostgreSQL.

## Features

- User registration and login
- Password hashing with bcrypt
- JWT-based authentication
- Admin and user roles
- Task CRUD with ownership checks
- `/api/me` for the current logged-in user
- `/health` health check endpoint
- Swagger docs at `/docs`

## Project Structure

```text
backend/
|-- app/
|   |-- main.py
|   |-- core/
|   |   |-- config.py
|   |   `-- security.py
|   |-- db/
|   |   |-- database.py
|   |   `-- models.py
|   |-- schemas/
|   |   |-- task.py
|   |   `-- user.py
|   `-- api/
|       |-- deps.py
|       `-- routes/
|           |-- auth.py
|           `-- tasks.py
|-- .env
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Setup

1. Create a PostgreSQL database named `task_management`.
2. Open the `backend` folder.
3. Create and activate a virtual environment.
4. Install dependencies.
5. Copy `.env.example` to `.env` and update the values.
6. Start the server.

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Environment Variables

```env
PROJECT_NAME=Task Management API
API_V1_PREFIX=/api
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_management
SECRET_KEY=replace-this-with-a-strong-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Main Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/me`
- `GET /api/users` - admin only
- `POST /api/tasks`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `PUT /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`
- `GET /health`

## Notes

- Passwords are never returned in API responses.
- Login uses email and password.
- Admin users can delete any task.
- Regular users can only access their own tasks.
