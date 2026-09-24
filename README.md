<<<<<<< HEAD
"# dineflow-restaurant-management" 
=======
# DineFlow - Restaurant Management System

A production-ready Restaurant Order & Kitchen Operations backend API built with **FastAPI**, **MongoDB** (PyMongo), and **JWT Authentication with Role-Based Access Control (RBAC)**.

---

## 📁 Project Structure

The project strictly follows the original consolidated file structure:

```
RK_SYSTEM/
├── app/
│   ├── config/
│   │   └── settings.py         # Application configuration & JWT settings
│   ├── database/
│   │   ├── mongodb.py          # MongoDB client & collection handles
│   │   └── indexes.py          # MongoDB indexing
│   ├── models/                 # Entity domain models (user, customer, order, etc.)
│   ├── routes/
│   │   ├── routes.py           # Consolidated API route endpoints & RBAC guards
│   │   └── __init__.py
│   ├── schemas/                # Request & response Pydantic schemas
│   ├── services/
│   │   ├── service.py          # Consolidated business-logic services & auth logic
│   │   └── __init__.py
│   └── main.py                 # FastAPI application entry point
├── tests/
│   └── test_api.py             # Automated API & RBAC test suite
├── seed_roles.py               # Database seeder for all 5 restaurant roles
├── requirements.txt            # Python dependencies (includes PyJWT & bcrypt)
├── .env.example                # Environment variables template
└── README.md
```

---

## 🔐 Authentication & Roles

The system uses **JWT Bearer Token Authentication** and **bcrypt password hashing**.

### User Roles & Permissions

| Role | Default Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **ADMIN** | `admin@dineflow.com` | `Password123!` | Full superuser access to all endpoints |
| **MANAGER** | `manager@dineflow.com` | `Password123!` | Users, customers, menu, inventory, tables, refund approvals |
| **CHEF** | `chef@dineflow.com` | `Password123!` | Kitchen tickets, events, inventory, recipes, menu items |
| **WAITER** | `waiter@dineflow.com` | `Password123!` | Orders, order items, tables, reservations, customers, feedback |
| **CASHIER** | `cashier@dineflow.com` | `Password123!` | Invoices, payments, order billing, refund requests |

### Authentication Endpoints

- `POST /api/auth/login`: Authenticate with email & password, receive Bearer JWT token.
- `POST /api/users/login`: Alias for login.
- `POST /api/auth/register`: Register new user and receive JWT token.
- `GET /api/auth/me`: Get profile of the currently logged-in user (requires Bearer token).

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Ensure `.env` contains:
```env
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=restaurant_management
APP_NAME=Restaurant Management System
DEBUG=True
JWT_SECRET_KEY=supersecretjwtkeyforrestaurantmanagementsystem2026
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Seed Default Role Accounts
```bash
python seed_roles.py
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```
- API Root: `http://127.0.0.1:8000`
- Swagger UI (Interactive Docs): `http://127.0.0.1:8000/docs`

### 5. Run Automated Tests
```bash
pytest tests/test_api.py -v
```
>>>>>>> 6f39839 (your commit message)
