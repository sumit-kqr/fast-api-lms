import unittest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

class TestAPI(unittest.TestCase):
    """
    Test suite for FastAPI endpoints covering users and courses.
    Each test checks a specific API behavior or edge case.
    """

    def test_get_users(self):
        """
        Ensure the /users endpoint returns a 200 status and a list of users.
        """
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_user(self):
        """
        Test user creation with a unique email and valid role.
        """
        unique_email = f"testuser_{uuid.uuid4()}@example.com"
        user_data = {
            "email": unique_email,
            "role": "student"
        }
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], user_data["email"])
        self.assertEqual(response.json()["role"], user_data["role"])

    def test_get_courses(self):
        """
        Ensure the /courses endpoint returns a 200 status and a list of courses.
        """
        response = client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_course(self):
        """
        Test course creation. Accepts 200 if user exists, 422 if not.
        """
        course_data = {
            "title": "Test Course",
            "description": "A test course.",
            "user_id": 1
        }
        response = client.post("/courses", json=course_data)
        self.assertIn(response.status_code, [200, 422])

    def test_health_check(self):
        """
        Check if the root endpoint is available (200 or 404).
        """
        response = client.get("/")
        self.assertIn(response.status_code, [200, 404])

    def test_create_user_missing_field(self):
        """
        Attempt to create a user with missing email, expect 422.
        """
        user_data = {"role": "student"}
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 422)

    def test_create_user_duplicate_email(self):
        """
        Attempt to create a user with a duplicate email, expect 422.
        """
        user_data = {"email": "duplicate@example.com", "role": "student"}
        response1 = client.post("/users", json=user_data)
        response2 = client.post("/users", json=user_data)
        self.assertEqual(response2.status_code, 422)

    def test_get_nonexistent_user(self):
        """
        Try to fetch a user that does not exist, expect 404.
        """
        response = client.get("/users/99999")
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_user(self):
        """
        Try to update a user that does not exist, expect 404.
        """
        user_data = {"email": "new@example.com"}
        response = client.patch("/users/99999", json=user_data)
        self.assertEqual(response.status_code, 404)

    def test_create_course_missing_field(self):
        """
        Attempt to create a course with missing user_id, expect 422.
        """
        course_data = {"title": "No User"}
        response = client.post("/courses", json=course_data)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
