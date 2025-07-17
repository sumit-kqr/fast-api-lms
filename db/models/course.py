from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SAEnum
from .mixins import Timestamp

class ContentType(str, Enum):
    lesson = "lesson"
    quiz = "quiz"
    assignment = "assignment"

class CourseBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")

class Course(CourseBase, Timestamp, table=True):
    __tablename__ = "courses"
    id: Optional[int] = Field(default=None, primary_key=True)

class CoursePublic(CourseBase):
    id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None

class SectionBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    course_id: int = Field(foreign_key="courses.id")

class Section(SectionBase, Timestamp, table=True):
    __tablename__ = "sections"
    id: Optional[int] = Field(default=None, primary_key=True)

class SectionPublic(SectionBase):
    id: int
    course_id: int

class SectionCreate(SectionBase):
    pass

class SectionUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None

class ContentBlockBase(SQLModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    type: ContentType = Field(sa_type=SAEnum(ContentType, name="content_type"))
    url: Optional[str] = None
    content: Optional[str] = None
    section_id: int = Field(foreign_key="sections.id")

class ContentBlock(ContentBlockBase, Timestamp, table=True):
    __tablename__ = "content_blocks"
    id: Optional[int] = Field(default=None, primary_key=True)

class ContentBlockPublic(ContentBlockBase):
    id: int
    section_id: int

class ContentBlockCreate(ContentBlockBase):
    pass

class ContentBlockUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ContentType] = None
    url: Optional[str] = None
    content: Optional[str] = None
    section_id: Optional[int] = None

class StudentCourseBase(SQLModel):
    student_id: int = Field(foreign_key="users.id")
    course_id: int = Field(foreign_key="courses.id")
    completed: bool = Field(default=False)

class StudentCourse(StudentCourseBase, Timestamp, table=True):
    __tablename__ = "student_courses"
    id: Optional[int] = Field(default=None, primary_key=True)

class StudentCoursePublic(StudentCourseBase):
    id: int

class StudentCourseCreate(StudentCourseBase):
    pass

class StudentCourseUpdate(SQLModel):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    completed: Optional[bool] = None

class CompletedContentBlockBase(SQLModel):
    student_id: int = Field(foreign_key="users.id")
    content_block_id: int = Field(foreign_key="content_blocks.id")
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: int = Field(default=0)

class CompletedContentBlock(CompletedContentBlockBase, Timestamp, table=True):
    __tablename__ = "completed_content_blocks"
    id: Optional[int] = Field(default=None, primary_key=True)

class CompletedContentBlockPublic(CompletedContentBlockBase):
    id: int

class CompletedContentBlockCreate(CompletedContentBlockBase):
    pass

class CompletedContentBlockUpdate(SQLModel):
    student_id: Optional[int] = None
    content_block_id: Optional[int] = None
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: Optional[int] = None