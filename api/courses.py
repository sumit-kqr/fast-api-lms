from typing import List, Annotated
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.db_setup import SessionDep
from db.models.course import Course, CourseCreate, CoursePublic, CourseUpdate, Section, SectionPublic

router = APIRouter(tags=['courses'])

@router.get("/courses", response_model=List[CoursePublic])
async def read_courses(session: SessionDep):
    courses = session.exec(select(Course)).all()
    return courses

@router.post("/courses", response_model=CoursePublic)
async def create_course_api(course: CourseCreate, session: SessionDep):
    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

@router.get("/courses/{id}", response_model=CoursePublic)
async def read_course(id: int, session: SessionDep):
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.patch("/courses/{id}", response_model=CoursePublic)
async def update_course(id: int, course: CourseUpdate, session: SessionDep):
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
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    session.delete(course)
    session.commit()
    return {"ok": True}

@router.get("/courses/{id}/sections", response_model=List[SectionPublic])
async def read_course_sections(id: int, session: SessionDep):
    course = session.get(Course, id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    sections = session.exec(select(Section).where(Section.course_id == id)).all()
    return sections