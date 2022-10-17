from flask_wtf import FlaskForm
from flask_login import current_user

from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 65), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    USERNAME_HINT = 'Username must begin with letter and only have letters, numbers, dot or underscores'
    PASSSWORD_HINT = 'Password confirmation must match'
    USERNAME_PATTERN = '^[A-Za-z][A-Za-z0-9_.]*$'

    email = StringField('Email', validators=[DataRequired(), Length(1, 65), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 65),
                                                   Regexp(USERNAME_PATTERN, 0, USERNAME_HINT)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message=PASSSWORD_HINT)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        from infrastructure.models.users import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered!')

    def validate_username(self, field):
        from infrastructure.models.users import User
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class EmailUpdatedForm(FlaskForm):
    current_email = StringField('Current Email', validators=[DataRequired(), Length(1, 65),
                                                             Email()])
    new_email = StringField('New Email', validators=[DataRequired(), Length(1, 65), Email()])
    submit = SubmitField('Submit')

    def validate_current_email(self, field):
        if current_user.email != field.data:
            raise ValidationError('Your current email is not correct')

    def validate_new_email(self, field):
        from infrastructure.models.users import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Can not register your new email')
