import unittest
import json
from fastapi.testclient import TestClient
from main import app

class TestHealthAndVersionEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_version_endpoint(self):
        response = self.client.get("/version")
        self.assertEqual(response.status_code, 200)
        self.assertIn("version", response.json())
        self.assertIsInstance(response.json()["version"], str)

if __name__ == "__main__":
    unittest.main()