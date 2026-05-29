# Field Force Manager — Backend

## Stack
- Python 3.10+
- Flask 3.x
- PostgreSQL 15+
- SQLAlchemy ORM
- Flask-Migrate (Alembic)
- Flask-CORS
- APScheduler (EOD cron job)
- python-dotenv

## Project structure

```
fieldforce/
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py        # db, cors, scheduler instances
│   ├── models/
│   │   ├── __init__.py
│   │   ├── staff.py
│   │   ├── client.py
│   │   ├── visit.py
│   │   ├── action_item.py
│   │   ├── follow_up.py
│   │   └── report.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── staff.py         # /api/staff
│   │   ├── clients.py       # /api/clients
│   │   ├── visits.py        # /api/visits
│   │   ├── action_items.py  # /api/action-items
│   │   ├── follow_ups.py    # /api/follow-ups
│   │   └── reports.py       # /api/reports
│   └── services/
│       ├── report_builder.py  # EOD report logic
│       └── scheduler.py       # Cron job setup
├── migrations/              # Alembic auto-generated
├── tests/
│   └── test_visits.py
├── .env.example
├── config.py
├── run.py
├── requirements.txt
└── schema.sql               # Raw SQL alternative to migrations
```

## Quick start

```bash
# 1. Clone and enter
cd fieldforce

# 2. Create virtualenv
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY

# 5. Create PostgreSQL database
createdb fieldforce_db

# 6. Run migrations
flask db init
flask db migrate -m "initial schema"
flask db upgrade

# 7. Seed a test staff member
python3 seed.py

# 8. Start server
python3 run.py
# Server runs at http://localhost:5000
```

## Environment variables (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5432/fieldforce_db
SECRET_KEY=change-this-to-a-random-string
FLASK_ENV=development
EOD_REPORT_TIME=19:00        # 7 PM IST — when cron fires
WHATSAPP_API_KEY=            # Phase 4 — leave blank for now
MANAGER_PHONE=               # Phase 4
```
