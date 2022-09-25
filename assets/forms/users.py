from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


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
