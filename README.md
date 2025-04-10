# 🧩 FastAPI User & Order Management API

A modern RESTful API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, designed to manage users and orders with secure JWT authentication and role-based access control.

---

## 🚀 Features

- 🔐 JWT-based authentication (login, register)
- 👥 Role-based access control (admin vs customer)
- 📦 Order creation, updates, and deletion
- 📄 Fully typed services using Pydantic & SQLAlchemy
- 📃 PostgreSQL + Alembic for migrations
- 💣 Docker support for PostgreSQL container
- 📨 RESTful routing with FastAPI

---

## 📁 Project Structure

```
├── alembic.ini
├── api
│   ├── auth.py
│   ├── orders.py
│   └── users.py
├── config
│   └── settings.py
├── database
│   ├── database.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── versions/
│   │   └── script.py.mako
│   └── models
│       ├── base.py
│       ├── orders.py
│       ├── privileges.py
│       ├── role_privileges.py
│       ├── roles.py
│       └── users.py
├── main.py
├── middleware
│   └── dependencies.py
├── security.py
├── services
│   ├── auth.py
│   ├── order.py
│   ├── role.py
│   └── user.py
├── validators
│   ├── auth.py
│   ├── orders.py
│   └── users.py
├── requirements.txt
└── README.md
```

---

## 💠 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-orders-api.git
cd fastapi-orders-api
```

### 2. Set up the PostgreSQL container

```bash
docker-compose up -d
```

Ensure your `docker-compose.yml` contains:

```yaml
version: '3.8'
services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
```

### 3. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Alembic migrations

```bash
alembic upgrade head
```

### 5. Start the FastAPI server

```bash
uvicorn main:app --reload
```

---

## 🔐 Authentication

- Register: `POST /users/register`
- Login: `POST /users/login`
- Pass returned **JWT token** as a Bearer token in `Authorization` header to access protected endpoints.

---

## 🧪 API Endpoints (Simplified)

### 👤 Users

| Method | Endpoint             | Access        | Description              |
|--------|----------------------|---------------|--------------------------|
| POST   | `/users/register`    | Public        | Register a new user      |
| POST   | `/users/login`       | Public        | Login and get JWT token  |
| GET    | `/users/me`          | Authenticated | Get current user profile |
| PUT    | `/users/me`          | Authenticated | Update user profile      |
| DELETE | `/users/me`          | Authenticated | Delete own account       |
| GET    | `/users`             | Admin only    | List all users           |

### 📦 Orders

| Method | Endpoint                | Access                  | Description                          |
|--------|-------------------------|-------------------------|--------------------------------------|
| POST   | `/orders`               | Authenticated           | Create a new order                   |
| GET    | `/orders/{id}`          | Owner or Admin          | Get order by ID                      |
| PUT    | `/orders/{id}`          | Owner or Admin          | Update order status                  |
| DELETE | `/orders/{id}`          | Owner or Admin          | Delete order                         |
| GET    | `/orders/me`            | Authenticated           | List current user's orders           |
| GET    | `/orders/users/{id}`    | Admin only              | List orders for a specific user      |
| GET    | `/orders`               | Admin only              | List all orders                      |

---

## 📟 Example: Create Order with Postman

1. Login and get JWT token.
2. Make a `POST /orders` request with Bearer token:

```json
{
  "total_amount": 150.0,
  "status": "pending"
}
```

3. Include in Headers:

```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

---

## 📚 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 📌 Future Enhancements

- ✅ Pagination & filtering
- ✅ Swagger & ReDoc auto docs
- 🔐 Refresh tokens & logout flow
- 🥚 Unit & integration testing
- 📊 Admin dashboard

---

## 📄 License

MIT License. Use freely.

---

## 🙌 Acknowledgments

Built with ❤️ by leveraging FastAPI and the best Python tools in the ecosystem.
