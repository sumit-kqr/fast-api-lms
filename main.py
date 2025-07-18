from fastapi import FastAPI

from api import users, courses, sections
from db.db_setup import engine
from db.models import user, course

def create_db_and_tables():
    user.SQLModel.metadata.create_all(engine)
    course.SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Fast API LMS",
    description="LMS for managing students and courses.",
    version="0.0.1",
    contact={
        "name": "Sumit",
        "email": "sumit@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()