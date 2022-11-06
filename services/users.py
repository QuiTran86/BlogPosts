from infrastructure.models.users import User


class UserService:

    def __init__(self):
        self._model = User

    def find_user_by_id(self, user_id):
        return self._model.query.filter_by(id=user_id).first()

    def find_user_by_username(self, username):
        return self._model.query.filter_by(username=username).first()

    def find_user_by_email(self, email):
        return self._model.query.filter_by(email=email).first()
