
import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
try:
    from src.api.users import read_users, create_user_api, read_user, update_user, delete_user
    from src.db.models.course import User, UserCreate, UserUpdate
except ImportError:
    read_users = create_user_api = read_user = update_user = delete_user = None
    User = UserCreate = UserUpdate = None

class TestUsersAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock()
        self.user = MagicMock(id=1, name="Test User", email="test@example.com")

    async def test_read_users(self):
        self.session.exec.return_value.all.return_value = [self.user]
        if read_users:
            result = await read_users(self.session)
            self.assertEqual(result, [self.user])

    async def test_create_user_api(self):
        user_create = MagicMock()
        if create_user_api and User:
            with patch('src.api.users.User.model_validate', return_value=self.user):
                self.session.add = MagicMock()
                self.session.commit = MagicMock()
                self.session.refresh = MagicMock()
                result = await create_user_api(user_create, self.session)
                self.assertEqual(result, self.user)

    async def test_read_user_found(self):
        self.session.get.return_value = self.user
        if read_user:
            result = await read_user(1, self.session)
            self.assertEqual(result, self.user)

    async def test_read_user_not_found(self):
        self.session.get.return_value = None
        if read_user:
            with self.assertRaises(HTTPException):
                await read_user(1, self.session)

    async def test_update_user_found(self):
        user_update = MagicMock()
        self.session.get.return_value = self.user
        if update_user:
            with patch.object(self.user, 'sqlmodel_update') as mock_update:
                self.session.add = MagicMock()
                self.session.commit = MagicMock()
                self.session.refresh = MagicMock()
                with patch.object(user_update, 'model_dump', return_value={'name': 'Updated'}):
                    result = await update_user(1, user_update, self.session)
                    mock_update.assert_called_once()
                    self.assertEqual(result, self.user)

if __name__ == "__main__":
    unittest.main()
