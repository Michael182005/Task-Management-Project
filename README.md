# Task Management System

A full-stack Task Management application built using FastAPI (backend) and HTML, CSS, and JavaScript (frontend).
This project demonstrates secure authentication, role-based access control, and CRUD operations with a clean and modular architecture.

---

## 🚀 Features

### 🔐 Authentication & Security

* User registration and login
* Password hashing using bcrypt
* JWT-based authentication
* Protected API routes

### 👥 Role-Based Access

* **User:**

  * Can manage only their own tasks
* **Admin:**

  * Can view all users
  * Can delete any task

### 📋 Task Management

* Create tasks
* View tasks
* Update tasks
* Delete tasks
* User-specific task access

### 🌐 Frontend

* Login and Register pages
* Dashboard for task management
* JWT token stored in localStorage
* API integration using Fetch API

---

## 🛠️ Tech Stack

### Backend:

* FastAPI
* PostgreSQL (or SQLite for local testing)
* SQLAlchemy
* Pydantic
* JWT (python-jose)
* Passlib (bcrypt)

### Frontend:

* HTML
* CSS
* JavaScript (Vanilla JS)

---

## 📁 Project Structure

```
task-management-project/
│── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env.example
│
│── frontend/
│   ├── index.html
│   ├── register.html
│   ├── dashboard.html
│   ├── style.css
│   ├── script.js
│
│── README.md
```

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup

```
cd backend

python -m venv env
source env/bin/activate      # Linux / Mac
env\Scripts\activate         # Windows

pip install -r requirements.txt
```

Create a `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost:5432/taskdb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

Run backend server:

```
uvicorn app.main:app --reload
```

---

### 🔹 Frontend Setup

No installation required.

Simply open:

```
frontend/index.html
```

---

## 📌 API Documentation

Swagger UI available at:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

* User registers with email and password
* Password is hashed before storing
* On login, a JWT token is generated
* Token is used in request headers:

```
Authorization: Bearer <token>
```

---

## 📋 API Endpoints

### Auth

* POST `/auth/register`
* POST `/auth/login`

### Tasks

* GET `/tasks/`
* POST `/tasks/`
* PUT `/tasks/{id}`
* DELETE `/tasks/{id}`

---

## 📈 Scalability Notes

* Modular backend architecture
* Environment-based configuration
* Easily extendable with:

  * Redis caching
  * Docker deployment
  * Microservices architecture
  * Load balancing

---

## ✅ Future Improvements

* Pagination for tasks
* Refresh tokens
* Logging and monitoring
* Enhanced UI

---

## 👨‍💻 Author

Built as part of an internship assignment for a backend developer role.
This project showcases API design, authentication, and scalable backend development practices.

---
