import unittest

from app import create_app
from infrastructure import db
from infrastructure.models.users import User


class TestUserPassword(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        user = User(password='cat')
        self.assertTrue(user.password_hash is not None)

    def test_password_unaccessible(self):
        user = User(password='cat')
        with self.assertRaises(AttributeError):
            _ = user.password

    def test_password_salts_is_random(self):
        user1 = User(password='cat')
        user2 = User(password='cat')
        self.assertTrue(user1.password_hash != user2.password_hash)

    def test_password_verification(self):
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))


