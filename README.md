# The SecureGate RBAC System

A standalone **Role-Based Access Control (RBAC)** service built with **FastAPI** and **SQLite**. It manages Users, Roles, and Permissions through a clean layered architecture, with JWT-based authentication and permission-driven route protection.

This project includes:

- Many-to-many schema: **Users ↔ Roles** and **Roles ↔ Permissions**
- `POST /login` to receive a JWT access token
- `GET /resource` protected by permission `READ_DATA`
- `POST /assign-role` protected by permission `ASSIGN_ROLE` (admin-only)
- Authorization middleware that:
  - Validates Bearer JWT
  - Loads the user's effective permissions (via roles)
  - Denies unauthorized requests with correct status codes

---

## Features

- User registration and login with JWT authentication
- Password hashing using bcrypt
- Role-Based Access Control with a many-to-many User ↔ Role ↔ Permission schema
- Custom authorization middleware that checks permissions on protected routes
- Auto-seeded database with default roles (Admin, User) and permissions (READ_DATA, DELETE_DATA,    ASSIGN_ROLE)
- Interactive API docs via FastAPI's built-in Swagger UI at /docs

---

## Data Model

SQLite tables:

- `users`
- `roles`
- `permissions`
- `user_roles` (join table)
- `role_permissions` (join table)

---

## Setup & Installation

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd securegate-rbac
```

### 2) Create and activate a virtualenv

```bash
python -m venv myenv
source myenv/Scripts/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment

Copy `.env.example` to `.env` (optional). Defaults are safe for local evaluation.

### 5) Run the server

```bash
uvicorn app.main:app --reload
```

The app will auto-create `securegate.db` (SQLite) and seed demo data on startup.

### 7) Explore the API

Open "URL"/docs for the interactive Swagger UI.

### 8) Explore the Database

Open SQLite Viewer and upload the database file there to view the database.

---

## Demo Users (Seeded)

| Username | Password  | Role   | Permissions |
|---------:|-----------|--------|-------------|
| admin    | admin123  | Admin  | READ_DATA, ASSIGN_ROLE, DELETE_DATA |
| abc      | abc123    | User   | READ_DATA   |

---
