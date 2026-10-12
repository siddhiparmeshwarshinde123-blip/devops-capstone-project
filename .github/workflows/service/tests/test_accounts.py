import unittest

from service import create_app


class TestAccountService(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_root_returns_service_info(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Account REST API Service")

    def test_create_account(self):
        response = self.client.post(
            "/accounts",
            json={"name": "Test Account", "email": "test@example.com"},
        )
        self.assertEqual(response.status_code, 201)

    def test_list_accounts(self):
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)

    def test_read_missing_account(self):
        response = self.client.get("/accounts/999")
        self.assertEqual(response.status_code, 404)

    def test_cors_headers(self):
        response = self.client.get(
            "/accounts",
            headers={"Origin": "http://example.com"},
        )
        self.assertIn("Access-Control-Allow-Origin", response.headers)

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertIn("X-Frame-Options", response.headers)


if __name__ == "__main__":
    unittest.main()
