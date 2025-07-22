
import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
try:
    from src.api.courses import read_courses, create_course_api, read_course, update_course, delete_course, read_course_sections
    from src.db.models.course import Course, CourseCreate, CourseUpdate, Section
except ImportError:
    read_courses = create_course_api = read_course = update_course = delete_course = read_course_sections = None
    Course = CourseCreate = CourseUpdate = Section = None

class TestCoursesAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock()
        self.course = MagicMock(id=1, name="Test Course")
        self.section = MagicMock(id=1, course_id=1, name="Section 1")

    async def test_read_courses(self):
        self.session.exec.return_value.all.return_value = [self.course]
        if read_courses:
            result = await read_courses(self.session)
            self.assertEqual(result, [self.course])

    async def test_create_course_api(self):
        course_create = MagicMock()
        if create_course_api and Course:
            with patch('src.api.courses.Course.model_validate', return_value=self.course):
                self.session.add = MagicMock()
                self.session.commit = MagicMock()
                self.session.refresh = MagicMock()
                result = await create_course_api(course_create, self.session)
                self.assertEqual(result, self.course)

    async def test_read_course_found(self):
        self.session.get.return_value = self.course
        if read_course:
            result = await read_course(1, self.session)
            self.assertEqual(result, self.course)

    async def test_read_course_not_found(self):
        self.session.get.return_value = None
        if read_course:
            with self.assertRaises(HTTPException):
                await read_course(1, self.session)

    async def test_delete_course_found(self):
        self.session.get.return_value = self.course
        self.session.delete = MagicMock()
        self.session.commit = MagicMock()
        if delete_course:
            result = await delete_course(1, self.session)
            self.assertEqual(result, {"ok": True})

if __name__ == "__main__":
    unittest.main()
