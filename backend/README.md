# WithYou Backend API

FastAPI backend for the WithYou patient care and memory management system.

## Features

- ✅ FastAPI framework
- ✅ SQLite database with SQLAlchemy ORM
- ✅ User management (patients and caregivers)
- ✅ Mood check-ins tracking
- ✅ Memory cards management
- ✅ Emergency contacts management
- ✅ CORS configured
- ✅ Auto-generated API documentation

## Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── database.py           # Database configuration and session
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas for validation
│   ├── crud.py               # CRUD operations
│   └── routes.py             # API endpoints
├── agents/                   # Agent-related code (future)
├── tools/                    # Tools and utilities (future)
├── main.py                   # FastAPI app entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── .gitignore                # Git ignore rules
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- pip or conda

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your settings (optional for development)
```

### 5. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The application uses SQLite for data persistence. The database file (`app.db`) is automatically created on first run.

### Database Tables

1. **users** - User accounts (patients and caregivers)
2. **mood_checkins** - Mood tracking data
3. **memory_cards** - Memories and stories
4. **emergency_contacts** - Emergency contact information

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Mood Check-ins
- `POST /mood-checkins/` - Create mood check-in
- `GET /users/{user_id}/mood-checkins/` - Get user's mood history
- `GET /mood-checkins/{checkin_id}` - Get specific check-in
- `DELETE /mood-checkins/{checkin_id}` - Delete check-in

### Memory Cards
- `POST /memory-cards/` - Create memory card
- `GET /users/{user_id}/memory-cards/` - Get user's memories
- `GET /memory-cards/{card_id}` - Get specific memory
- `PUT /memory-cards/{card_id}` - Update memory
- `DELETE /memory-cards/{card_id}` - Delete memory

### Emergency Contacts
- `POST /emergency-contacts/` - Create emergency contact
- `GET /users/{user_id}/emergency-contacts/` - Get user's contacts
- `GET /emergency-contacts/{contact_id}` - Get specific contact
- `PUT /emergency-contacts/{contact_id}` - Update contact
- `DELETE /emergency-contacts/{contact_id}` - Delete contact

## Development

### Adding New Models

1. Create model in `app/models.py`
2. Create Pydantic schema in `app/schemas.py`
3. Add CRUD operations in `app/crud.py`
4. Add routes in `app/routes.py`

### Running Tests (Future)

```bash
pytest
```

## Next Steps

- [ ] Add authentication/authorization
- [ ] Add route protection with JWT tokens
- [ ] Add input validation enhancements
- [ ] Add logging
- [ ] Add error handling middleware
- [ ] Add database migration support (Alembic)
- [ ] Add integration with Agent Framework
- [ ] Add testing suite

## Troubleshooting

### Port Already in Use
Change the port in the command:
```bash
uvicorn main:app --reload --port 8001
```

### Module Not Found
Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Issues
Delete `app.db` to reset the database:
```bash
rm app.db
```

## License

Part of the WithYou project.
