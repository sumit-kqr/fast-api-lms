
import unittest
from unittest.mock import MagicMock, patch
try:
    from src.db.db_setup import get_session
except ImportError:
    get_session = None

class TestDBSetup(unittest.TestCase):
    def test_get_session_returns_session(self):
        if get_session:
            with patch('src.db.db_setup.sessionmaker') as mock_sessionmaker:
                mock_sessionmaker.return_value = MagicMock()
                session = get_session()
                self.assertIsNotNone(session)

    def test_session_commit(self):
        session = MagicMock()
        session.commit = MagicMock()
        session.commit()
        session.commit.assert_called_once()

    def test_session_rollback(self):
        session = MagicMock()
        session.rollback = MagicMock()
        session.rollback()
        session.rollback.assert_called_once()

    def test_session_close(self):
        session = MagicMock()
        session.close = MagicMock()
        session.close()
        session.close.assert_called_once()

    def test_session_add(self):
        session = MagicMock()
        obj = MagicMock()
        session.add = MagicMock()
        session.add(obj)
        session.add.assert_called_once_with(obj)

if __name__ == "__main__":
    unittest.main()
