from .. import db
from domain.permission import Permission


class Role(db.Model):
    Roles = {
        'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
        'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
        'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
                  Permission.MODERATE, Permission.ADMIN],
    }

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_role():
        default_role = 'User'
        for role_name in Role.Roles:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
            role.reset_permission()
            for perm in Role.Roles[role_name]:
                role.add_permission(perm)
            role.default = role_name == default_role
            db.session.add(role)
        db.session.commit()

    def reset_permission(self):
        self.permissions = 0

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def has_permission(self, permission):
        return self.permissions & permission == permission
