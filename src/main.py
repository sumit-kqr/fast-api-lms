from fastapi import FastAPI
from src.api import users, courses, sections
from src.db.db_setup import engine
from src.db.models import user, course

def create_db_and_tables():
    """Create all database tables for users and courses if they do not exist."""
    user.SQLModel.metadata.create_all(engine)
    course.SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="FastAPI LMS",
    description="A Learning Management System for managing students and courses.",
    version="0.0.1",
    contact={"name": "Sumit", "email": "sumit@example.com"},
    license_info={"name": "MIT"},
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)

@app.on_event("startup")
def on_startup():
    """Initialize database tables on application startup."""
    create_db_and_tables()