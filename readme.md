# Finance Data Processing and Access Control Backend

A Django REST Framework backend for a finance dashboard system with 
role-based access control, financial record management, and analytics APIs.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Framework | Django + Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | SQLite |
| CORS | django-cors-headers |

---

## Project Structure
```
finance-backend/
├── finance_backend/   # Core settings, URLs, exception handler
├── users/             # User model, roles, auth APIs
├── records/           # Financial records CRUD APIs
├── dashboard/         # Summary and analytics APIs
├── manage.py
└── requirements.txt
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Madhav-Sharma-2003/finance-backend.git
cd finance-backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

Server will run at: `http://127.0.0.1:8000`

---

## Roles & Permissions

| Action | Viewer | Analyst | Admin |
|---|---|---|---|
| View own records | ✅ | ✅ | ✅ |
| View all records | ❌ | ✅ | ✅ |
| Create records | ❌ | ✅ | ✅ |
| Update records | ❌ | ✅ | ✅ |
| Delete records | ❌ | ❌ | ✅ |
| View dashboard summary | ✅ | ✅ | ✅ |
| View analytics | ❌ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## API Reference

### Auth Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/users/register/` | Public | Register new user |
| POST | `/api/users/login/` | Public | Login, get JWT tokens |
| POST | `/api/users/token/refresh/` | Public | Refresh access token |
| GET | `/api/users/profile/` | All roles | Get current user profile |
| GET | `/api/users/all/` | Admin | List all users |
| PUT | `/api/users/<id>/update/` | Admin | Update user role/status |

### Records Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/records/` | All roles | List records (filtered by role) |
| POST | `/api/records/` | Analyst, Admin | Create new record |
| GET | `/api/records/<id>/` | All roles | Get single record |
| PUT | `/api/records/<id>/` | Analyst, Admin | Update record |
| DELETE | `/api/records/<id>/` | Admin | Soft delete record |

#### Filtering Support
```
GET /api/records/?type=income
GET /api/records/?category=food
GET /api/records/?start=2024-01-01&end=2024-03-31
GET /api/records/?type=expense&category=rent
```

### Dashboard Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/dashboard/summary/` | All roles | Total income, expense, net balance |
| GET | `/api/dashboard/categories/` | All roles | Category-wise breakdown |
| GET | `/api/dashboard/trends/` | All roles | Monthly income vs expense trend |
| GET | `/api/dashboard/recent/` | All roles | Last 10 transactions |
| GET | `/api/dashboard/analytics/` | Analyst, Admin | Deep insights, month comparison |

---

## Request & Response Examples

### Register
```
POST /api/users/register/
Content-Type: application/json

{
    "username": "john",
    "email": "john@example.com",
    "password": "john1234",
    "role": "analyst"
}
```
Response:
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "role": "analyst",
        "is_active": true
    },
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

### Create Record
```
POST /api/records/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "amount": "50000.00",
    "type": "income",
    "category": "salary",
    "date": "2024-03-01",
    "notes": "March salary"
}
```

### Dashboard Summary Response
```json
{
    "total_income": 55000.00,
    "total_expense": 20000.00,
    "net_balance": 35000.00,
    "total_records": 5,
    "status": "profit"
}
```

### Error Response Format
All errors follow a consistent format:
```json
{
    "success": false,
    "status_code": 400,
    "error": "amount: Amount must be greater than zero."
}
```

---

## Assumptions Made

1. **Roles are assigned at registration** — any role can be passed 
   during register. In production, admin creation would be restricted.

2. **Soft delete** — records are never permanently deleted. 
   `is_deleted=True` flag is set instead, preserving financial history.

3. **Viewer scope** — viewers can only see their own records and 
   dashboard data scoped to their own transactions.

4. **SQLite for simplicity** — chosen deliberately for easy local 
   setup without any database configuration. Can be swapped to 
   PostgreSQL by changing `DATABASES` in settings.py.

5. **Categories are predefined** — a fixed list of categories is 
   used to maintain data consistency. Can be made dynamic via a 
   separate Category model if needed.

6. **Date validation** — future dates are rejected. Records older 
   than 10 years are also rejected as they are likely data entry errors.

---

## Tradeoffs Considered

| Decision | Chosen Approach | Alternative |
|---|---|---|
| Database | SQLite | PostgreSQL (production ready) |
| Role storage | Field on User model | Separate Role/Permission table |
| Delete behavior | Soft delete | Hard delete |
| Auth | JWT | Session based auth |
| API style | REST | GraphQL |

---

## Optional Enhancements Implemented

- ✅ JWT Authentication
- ✅ Soft delete for records
- ✅ Filtering by type, category, date range
- ✅ Global consistent error handling
- ✅ Role-based data scoping on dashboard

---

## Author

**Madhav Sharma**  
MCA Student  
GitHub: https://github.com/Madhav-Sharma-2003
```
