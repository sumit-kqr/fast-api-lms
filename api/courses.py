from typing import List, Annotated
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.db_setup import SessionDep
from db.models.course import Course, CourseCreate, CoursePublic, CourseUpdate, Section, SectionPublic

router = APIRouter(tags=['courses'])

@router.get("/courses", response_model=List[CoursePublic])
async def read_courses(session: SessionDep):
    """
    Retrieve a list of all courses in the system.
    Returns a list of course objects.
    """
    courses = session.exec(select(Course)).all()
    return courses

@router.post("/courses", response_model=CoursePublic)
async def create_course_api(course: CourseCreate, session: SessionDep):
    """
    Create a new course with the provided information.
    Returns the created course object.
    """
    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@router.get("/courses/{id}", response_model=CoursePublic)
async def read_course(id: int, session: SessionDep):
    """
    Retrieve a course by its unique ID.
    Returns the course object if found, otherwise raises 404.
    """
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.patch("/courses/{id}", response_model=CoursePublic)
async def update_course(id: int, course: CourseUpdate, session: SessionDep):
    """
    Update an existing course's information by ID.
    Returns the updated course object. Raises 404 if not found.
    """
    db_course = session.get(Course, id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    course_data = course.model_dump(exclude_unset=True)
    db_course.sqlmodel_update(course_data)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@router.delete("/courses/{id}")
async def delete_course(id: int, session: SessionDep):
    """
    Delete a course by its unique ID.
    Returns a confirmation if successful, otherwise raises 404.
    """
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(course)
    session.commit()
    return {"ok": True}

@router.get("/courses/{id}/sections", response_model=List[SectionPublic])
async def read_course_sections(id: int, session: SessionDep):
    """
    Retrieve all sections for a given course by course ID.
    Returns a list of section objects. Raises 404 if course not found.
    """
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    sections = session.exec(select(Section).where(Section.course_id == id)).all()
    return sections