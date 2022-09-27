import unittest

from flask import current_app
from infrastructure import db
from app import create_app


class TestCreateAppCtx(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app('testing')
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        self.app_ctx.pop()

    def test_current_app(self):
        self.assertFalse(current_app is None)

    def test_app_config(self):
        self.assertTrue(current_app.config['TESTING'])
