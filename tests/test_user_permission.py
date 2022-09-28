import unittest

from app import create_app
from infrastructure import db
from infrastructure.models.users import User, AnonymousUser
from domain.permission import Permission


class TestUserPermission(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_normal_user_permission(self):
        user = User(name='john', email='john@gmail.com')
        self.assertTrue(user.can_do(Permission.WRITE))
        self.assertTrue(user.can_do(Permission.FOLLOW))
        self.assertTrue(user.can_do(Permission.COMMENT))
        self.assertFalse(user.can_do(Permission.MODERATE))
        self.assertFalse(user.can_do(Permission.ADMIN))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can_do(Permission.WRITE))
        self.assertFalse(user.can_do(Permission.FOLLOW))
        self.assertFalse(user.can_do(Permission.COMMENT))
        self.assertFalse(user.can_do(Permission.MODERATE))
        self.assertFalse(user.can_do(Permission.ADMIN))
