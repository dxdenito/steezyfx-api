# WELCOME TO STEEZY FX

Steezy fx is a one stop platform for all your forex needs. 
We have a wide variety of tools, a ton of education and resources that you need in your forex journey.

**Live API:** (coming soon)
**Docs:** (coming soon) 
**GitHub:** (coming soon)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14.6 |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT |
| Testing | pytest + httpx |
| Linting | PEP8 |

---

## Setup

```bash
# Clone the repo
git clone https://github.com/dxdenito/steezyfx-api.git
cd steezyfx-api

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your values

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

---

## Developer

**Denis Kibathi Karanja**  
Nairobi, Kenya  
GitHub: [@dxdenito](https://github.com/dxdenito)  
LinkedIn: [denis-karanja-184481110](https://www.linkedin.com/in/denis-karanja-184481110/)