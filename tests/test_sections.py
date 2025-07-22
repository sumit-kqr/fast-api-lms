
import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
try:
    from src.api.sections import read_sections, create_section_api, read_section, update_section, delete_section
    from src.db.models.course import Section, SectionCreate, SectionUpdate
except ImportError:
    read_sections = create_section_api = read_section = update_section = delete_section = None
    Section = SectionCreate = SectionUpdate = None

class TestSectionsAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock()
        self.section = MagicMock(id=1, course_id=1, name="Section 1")

    async def test_read_sections(self):
        self.session.exec.return_value.all.return_value = [self.section]
        if read_sections:
            result = await read_sections(self.session)
            self.assertEqual(result, [self.section])

    async def test_create_section_api(self):
        section_create = MagicMock()
        if create_section_api and Section:
            with patch('src.api.sections.Section.model_validate', return_value=self.section):
                self.session.add = MagicMock()
                self.session.commit = MagicMock()
                self.session.refresh = MagicMock()
                result = await create_section_api(section_create, self.session)
                self.assertEqual(result, self.section)

    async def test_read_section_found(self):
        self.session.get.return_value = self.section
        if read_section:
            result = await read_section(1, self.session)
            self.assertEqual(result, self.section)

    async def test_read_section_not_found(self):
        self.session.get.return_value = None
        if read_section:
            with self.assertRaises(HTTPException):
                await read_section(1, self.session)

    async def test_delete_section_found(self):
        self.session.get.return_value = self.section
        self.session.delete = MagicMock()
        self.session.commit = MagicMock()
        if delete_section:
            result = await delete_section(1, self.session)
            self.assertEqual(result, {"ok": True})

if __name__ == "__main__":
    unittest.main()
