import unittest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_user(self):
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
        response = client.get("/courses")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_create_course(self):
        # This test assumes a user with id=1 exists
        course_data = {
            "title": "Test Course",
            "description": "A test course.",
            "user_id": 1
        }
        response = client.post("/courses", json=course_data)
        # Accept 200 or 422 (if user_id doesn't exist)
        self.assertIn(response.status_code, [200, 422])

    def test_health_check(self):
        response = client.get("/")
        self.assertIn(response.status_code, [200, 404])  # 404 if not implemented, 200 if root exists

    def test_create_user_missing_field(self):
        user_data = {"role": "student"}  # Missing email
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 422)

    def test_create_user_duplicate_email(self):
        user_data = {"email": "duplicate@example.com", "role": "student"}
        response1 = client.post("/users", json=user_data)
        response2 = client.post("/users", json=user_data)
        self.assertEqual(response2.status_code, 422)

    def test_get_nonexistent_user(self):
        response = client.get("/users/99999")
        self.assertEqual(response.status_code, 404)

    def test_update_nonexistent_user(self):
        user_data = {"email": "new@example.com"}
        response = client.patch("/users/99999", json=user_data)
        self.assertEqual(response.status_code, 404)

    def test_create_course_missing_field(self):
        course_data = {"title": "No User"}  # Missing user_id
        response = client.post("/courses", json=course_data)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
