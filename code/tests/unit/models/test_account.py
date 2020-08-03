from datetime import datetime
from unittest import TestCase
from app.api.models.account import AccountModel


class AccountTest(TestCase):
    def test_create_account(self):
        account = AccountModel(
            email="test_email@sample.com", password="some_password", type="user"
        )

        self.assertEqual(account.id, None)
        self.assertEqual(account.email, "test_email@sample.com")
        self.assertEqual(account.password, "some_password")
        self.assertEqual(account.type, "user")

    def test_account_json(self):
        account = AccountModel(
            email="test_email@sample.com", password="some_password", type="user"
        )
        account.created_at = datetime(2020, 8, 2, 8, 30, 0)
        account.updated_at = datetime(2020, 8, 2, 8, 30, 0)
        expected_output = {
            "id": None,
            "email": "test_email@sample.com",
            "password": "some_password",
            "type": "user",
            "created_at": "2020-08-02 08:30:00",
            "updated_at": "2020-08-02 08:30:00",
        }
        self.assertEqual(
            account.json(),
            expected_output,
            f"Expected JSON value: {expected_output}\n" f"But given: {account.json()}",
        )
