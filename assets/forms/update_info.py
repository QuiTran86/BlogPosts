from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Length, DataRequired, Regexp, ValidationError

from infrastructure.models.roles import Role
from infrastructure.models.users import User


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 63)])
    location = StringField('Location', validators=[Length(0, 63)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    USERNAME_PATTERN = '^[a-zA-Z][a-zA-Z0-9_.]*$'
    USERNAME_HINT = 'Username must begin with letter and only have letters, number, dors or' \
                    'underscores'
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp(USERNAME_PATTERN, 0, USERNAME_HINT)])
    confirmed = BooleanField('Confirm')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0, 63)])
    location = StringField('Location', validators=[Length(0, 63)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('The email was already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('The username was already registered.')
