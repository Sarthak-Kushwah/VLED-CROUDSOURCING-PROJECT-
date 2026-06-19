# FAQFusion AI — Backend

AI-powered FAQ management system that automatically answers repeated questions using NLP similarity matching and maintains a growing knowledge repository.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask 3.x with Blueprint architecture |
| Database | MySQL 8+ via SQLAlchemy ORM |
| AI Engine | Sentence Transformers (`all-MiniLM-L6-v2`) + scikit-learn cosine similarity |
| Auth | Werkzeug password hashing + Flask sessions (JWT-ready) |
| Validation | Custom validators with Marshmallow-style patterns |

## Project Structure

```
FAQFusion-AI/
├── .env                          # Environment variables (DO NOT commit)
├── requirements.txt              # Python dependencies
├── backend/
│   ├── __init__.py
│   ├── app.py                    # Application factory (create_app)
│   ├── config.py                 # Configuration classes
│   ├── manage.py                 # CLI: create-admin, seed-faqs
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── faq.py                # FAQ model
│   │   ├── question.py           # Question model (with status lifecycle)
│   │   └── admin.py              # Admin model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py        # /register, /login, /logout
│   │   ├── faq_routes.py         # /faqs, /faq/<id>, CRUD
│   │   ├── question_routes.py    # /ask-question
│   │   └── admin_routes.py       # /pending-questions, /approve-question
│   ├── services/
│   │   ├── __init__.py
│   │   └── similarity_engine.py  # AI NLP matching engine
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py         # @login_required, @admin_required
│       └── validators.py         # Input validation functions
└── database/
    ├── __init__.py
    ├── db.py                     # SQLAlchemy instance & init_db()
    └── schema.sql                # MySQL schema for manual setup
```

## Quick Start

### 1. Prerequisites

- Python 3.10+
- MySQL 8.0+

### 2. Create MySQL Database

```sql
CREATE DATABASE faqfusion_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or run the full schema:

```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure Environment

Edit `.env` with your MySQL credentials:

```env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/faqfusion_db
SECRET_KEY=your-production-secret-key
SIMILARITY_THRESHOLD=0.75
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create Admin User

```bash
python -m backend.manage create-admin
```

### 6. Seed Sample FAQs (optional)

```bash
python -m backend.manage seed-faqs
```

### 7. Run the Server

```bash
flask --app backend.app run --debug
```

The API will be available at `http://127.0.0.1:5000`.

## API Reference

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | Public | Register a new user |
| POST | `/login` | Public | Login (user or admin) |
| POST | `/logout` | User | End session |

### Questions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/ask-question` | User | Submit a question (AI auto-answers if possible) |

### FAQ Management

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/faqs` | Public | List FAQs (search, filter, paginate) |
| GET | `/faq/<id>` | Public | Get single FAQ |
| POST | `/faq/add` | Admin | Create FAQ |
| PUT | `/faq/update/<id>` | Admin | Update FAQ |
| DELETE | `/faq/delete/<id>` | Admin | Soft-delete FAQ |

### Admin

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/pending-questions` | Admin | List pending questions |
| POST | `/approve-question/<id>` | Admin | Approve & optionally convert to FAQ |
| POST | `/reject-question/<id>` | Admin | Reject a pending question |

### System

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | Public | Health check |

## AI Similarity Engine

The engine uses **Sentence Transformers** (`all-MiniLM-L6-v2`) to encode questions into 384-dimensional dense vectors, then computes **cosine similarity** against all active FAQs.

- **Threshold** (default `0.75`): configurable via `.env` → `SIMILARITY_THRESHOLD`
- **Auto-answer**: If similarity ≥ threshold, the FAQ answer is returned immediately
- **Pending review**: If similarity < threshold, the question is queued for admin review

## Future Enhancements

- JWT-based authentication (decorators are already JWT-ready)
- Rate limiting with Flask-Limiter
- FAQ embedding caching with Redis
- WebSocket notifications for admin queue
- Bulk FAQ import/export (CSV/Excel via Pandas)
