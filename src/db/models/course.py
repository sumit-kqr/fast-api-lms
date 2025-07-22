from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Enum as SAEnum
from .mixins import Timestamp

class ContentType(str, Enum):
    """Enum for content block types: lesson, quiz, or assignment."""
    lesson = "lesson"
    quiz = "quiz"
    assignment = "assignment"

class CourseBase(SQLModel):
    """Base model for course data."""
    title: str = Field(max_length=200)
    description: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")

class Course(CourseBase, Timestamp, table=True):
    """SQLModel table for courses."""
    __tablename__ = "courses"
    id: Optional[int] = Field(default=None, primary_key=True)

class CoursePublic(CourseBase):
    """Public schema for course data."""
    id: int

class CourseCreate(CourseBase):
    """Schema for creating a new course."""
    pass

class CourseUpdate(SQLModel):
    """Schema for updating course fields."""
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None

class SectionBase(SQLModel):
    """Base model for section data."""
    title: str = Field(max_length=200)
    description: Optional[str] = None
    course_id: int = Field(foreign_key="courses.id")

class Section(SectionBase, Timestamp, table=True):
    """SQLModel table for sections."""
    __tablename__ = "sections"
    id: Optional[int] = Field(default=None, primary_key=True)

class SectionPublic(SectionBase):
    """Public schema for section data."""
    id: int
    course_id: int

class SectionCreate(SectionBase):
    """Schema for creating a new section."""
    pass

class SectionUpdate(SQLModel):
    """Schema for updating section fields."""
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None

class ContentBlockBase(SQLModel):
    """Base model for content block data."""
    title: str = Field(max_length=200)
    description: Optional[str] = None
    type: ContentType = Field(sa_type=SAEnum(ContentType, name="content_type"))
    url: Optional[str] = None
    content: Optional[str] = None
    section_id: int = Field(foreign_key="sections.id")

class ContentBlock(ContentBlockBase, Timestamp, table=True):
    """SQLModel table for content blocks."""
    __tablename__ = "content_blocks"
    id: Optional[int] = Field(default=None, primary_key=True)

class ContentBlockPublic(ContentBlockBase):
    """Public schema for content block data."""
    id: int
    section_id: int

class ContentBlockCreate(ContentBlockBase):
    """Schema for creating a new content block."""
    pass

class ContentBlockUpdate(SQLModel):
    """Schema for updating content block fields."""
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ContentType] = None
    url: Optional[str] = None
    content: Optional[str] = None
    section_id: Optional[int] = None

class StudentCourseBase(SQLModel):
    """Base model for student-course enrollment data."""
    student_id: int = Field(foreign_key="users.id")
    course_id: int = Field(foreign_key="courses.id")
    completed: bool = Field(default=False)

class StudentCourse(StudentCourseBase, Timestamp, table=True):
    """SQLModel table for student-course enrollments."""
    __tablename__ = "student_courses"
    id: Optional[int] = Field(default=None, primary_key=True)

class StudentCoursePublic(StudentCourseBase):
    """Public schema for student-course enrollment data."""
    id: int

class StudentCourseCreate(StudentCourseBase):
    """Schema for creating a new student-course enrollment."""
    pass

class StudentCourseUpdate(SQLModel):
    """Schema for updating student-course enrollment fields."""
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    completed: Optional[bool] = None

class CompletedContentBlockBase(SQLModel):
    """Base model for completed content block data."""
    student_id: int = Field(foreign_key="users.id")
    content_block_id: int = Field(foreign_key="content_blocks.id")
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: int = Field(default=0)

class CompletedContentBlock(CompletedContentBlockBase, Timestamp, table=True):
    """SQLModel table for completed content blocks."""
    __tablename__ = "completed_content_blocks"
    id: Optional[int] = Field(default=None, primary_key=True)

class CompletedContentBlockPublic(CompletedContentBlockBase):
    """Public schema for completed content block data."""
    id: int

class CompletedContentBlockCreate(CompletedContentBlockBase):
    """Schema for creating a new completed content block."""
    pass

class CompletedContentBlockUpdate(SQLModel):
    """Schema for updating completed content block fields."""
    student_id: Optional[int] = None
    content_block_id: Optional[int] = None
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: Optional[int] = None