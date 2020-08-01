from app.api.models.account import AccountModel
from ...base_test import BaseTest


class AccountTest(BaseTest):
    def test_crud_account(self):
        with self.app_context():
            account = AccountModel(email="test_email@email.com",
                                   password="somepassword",
                                   type="user")
            self.assertIsNone(AccountModel.find_by_email(email="test_email@email.com"),
                              "email: test_email@email.com was already registered in the DB.")
            account.register()
            self.assertIsNotNone(AccountModel.find_by_email(email="test_email@email.com"),
                                 "Expected output is test_email@email.com but recieves None.")
            account.remove_from_db()
            self.assertIsNone(AccountModel.find_by_email(email="test_email@email.com"),
                              "Expected output is None but recieves test_email@email.com.")