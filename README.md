# 📚 Bookly – Books & Reviews REST API

Bookly is a **production-ready, asynchronous REST API** built with **FastAPI** for managing a book catalog, user reviews, and categorization tags. The project implements **stateful JWT authentication** with Redis-based token revocation, asynchronous background processing using Celery, database migrations through Alembic, and a clean service-oriented architecture.

Designed with scalability and maintainability in mind, Bookly demonstrates industry-standard backend development practices including authentication, authorization, asynchronous programming, background task processing, centralized exception handling, and layered application architecture.

---

# ✨ Features

## 🔐 Authentication & Authorization

- User registration with email verification
- Secure login using JWT Access & Refresh Tokens
- Stateful authentication with Redis token revocation
- Logout support through token blocklisting
- Password reset via email verification links
- Role-Based Access Control (RBAC)
- Secure password hashing using Bcrypt

---

## 📚 Book Management

- Create books
- Retrieve all books
- Fetch book details
- Update existing books
- Delete books
- Associate books with authenticated users

---

## ⭐ Review Management

- Add reviews for books
- Update reviews
- Delete reviews
- Review ownership protection
- Rating validation (1–5)

---

## 🏷️ Tag Management

- Create tags
- Assign tags to books
- Many-to-many relationship between Books and Tags
- Retrieve books by tags

---

## ⚙️ Infrastructure Features

- Asynchronous FastAPI endpoints
- Celery background workers
- Redis caching & token storage
- Alembic database migrations
- Global exception handlers
- Request logging middleware
- Environment-based configuration
- Modular service architecture

---

# 🛠 Tech Stack

## Backend

- Python 3.11+
- FastAPI
- Uvicorn

---

## Database

- PostgreSQL
- SQLModel
- SQLAlchemy
- Alembic

---

## Authentication & Security

- JWT (PyJWT)
- Bcrypt
- ItsDangerous

---

## Background Processing

- Celery
- Redis

---

## Email

- FastAPI-Mail

---

## Configuration

- Pydantic Settings

---

## Async Utilities

- Asgiref

---

# 📂 Project Structure

```text
src/
│
├── auth/
│   ├── dependencies.py
│   ├── routes.py
│   ├── schemas.py
│   ├── service.py
│   └── utils.py
│
├── books/
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
│
├── reviews/
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
│
├── tags/
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
│
├── db/
│   ├── main.py
│   ├── models.py
│   └── redis_client.py
│
├── celery_tasks.py
├── config.py
├── errors.py
├── mail.py
├── middleware.py
└── main.py
```

---

# 🏗 Architecture Overview

```text
                    Client
                       │
                       ▼
                 FastAPI Routes
                       │
                       ▼
                 Service Layer
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      PostgreSQL     Redis       Celery
          │             │            │
          │             │            ▼
          │             │      Email Tasks
          │             │
          ▼             ▼
      SQLModel      Token Blocklist
```

---

# 🔑 Authentication Flow

```text
User Registration
        │
        ▼
 Password Hashing
        │
        ▼
 Store User in PostgreSQL
        │
        ▼
Generate Verification Link
        │
        ▼
 Celery Background Task
        │
        ▼
 Verification Email
        │
        ▼
 Verify Account
        │
        ▼
 Login
        │
        ▼
Access Token + Refresh Token
```

---

# 🔄 Logout Flow

```text
User Logout
      │
      ▼
Access Token
      │
      ▼
Store Token in Redis Blocklist
      │
      ▼
Future Requests
      │
      ▼
Token Exists?
      │
   Yes ▼ No
 Reject   Continue
```

---

# 📦 Technology Breakdown

| Technology | Purpose |
|------------|---------|
| FastAPI | Asynchronous REST API framework |
| PostgreSQL | Primary relational database |
| SQLModel | ORM and data validation |
| SQLAlchemy | Database abstraction layer |
| Alembic | Database migrations |
| Redis | Token blocklist and Celery broker |
| Celery | Background task execution |
| JWT | Authentication |
| Bcrypt | Password hashing |
| FastAPI-Mail | Email sending |
| Pydantic Settings | Configuration management |
| Uvicorn | ASGI server |

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bookly.git

cd bookly
```

---

## 2. Create Virtual Environment

### Linux/macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@localhost:5432/bookly

JWT_SECRET=your_super_secure_jwt_secret

JWT_ALGORITHM=HS256

REDIS_URL=redis://default:PASSWORD@HOST:PORT

DOMAIN=127.0.0.1:8000

MAIL_USERNAME=your_email

MAIL_PASSWORD=your_password

MAIL_FROM=noreply@bookly.com

MAIL_PORT=587

MAIL_SERVER=smtp.gmail.com

MAIL_STARTTLS=True

MAIL_SSL_TLS=False
```

---

# 🗄 Database Migration

Apply the latest database schema.

```bash
alembic upgrade head
```

---

# ⚡ Start Redis

Ensure Redis is running before starting the application.

Example:

```bash
redis-server
```

---

# 📨 Start Celery Worker

### Linux/macOS

```bash
celery -A src.celery_tasks.c_app worker --loglevel=info
```

### Windows

```bash
celery -A src.celery_tasks.c_app worker --pool=solo --loglevel=info
```

---

# ▶️ Run the API

```bash
uvicorn src:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/v1/docs
```

ReDoc

```
http://127.0.0.1:8000/api/v1/redoc
```

---

# 🔒 Security Features

- JWT Authentication
- Refresh Tokens
- Stateful Logout
- Redis Token Revocation
- Password Hashing using Bcrypt
- Email Verification
- Password Reset
- Role-Based Authorization
- Request Validation
- Global Exception Handling

---

# 📌 API Modules

| Module | Description |
|---------|-------------|
| Authentication | Login, Register, Logout, Password Reset |
| Books | CRUD operations for books |
| Reviews | Book reviews and ratings |
| Tags | Categorization system |
| Middleware | Logging and request processing |
| Mail | Email verification and password reset |
| Database | PostgreSQL and Redis configuration |

---

# 📈 Future Improvements

- Docker & Docker Compose support
- Unit and Integration Testing
- GitHub Actions CI/CD
- API Rate Limiting
- Pagination & Filtering
- Search functionality
- Book recommendations
- File uploads for book covers
- Social authentication (Google/GitHub)
- OpenAPI client generation

---

# 👨‍💻 Author

Developed with ❤️ using **FastAPI**, **PostgreSQL**, **Redis**, and **Celery**.
