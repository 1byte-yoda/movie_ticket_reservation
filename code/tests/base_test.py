"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for inheritance of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import create_app
from db import db

app = create_app(config_name="testing")

class BaseTest(TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
