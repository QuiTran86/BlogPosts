from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class PasswordUpdateForm(FlaskForm):
    MESSAGE_NEW_PASSWORD_CONFIRMED = 'Should match to desired password.'

    password1 = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password',
                              validators=[DataRequired(), EqualTo('password1',
                                                                  message=MESSAGE_NEW_PASSWORD_CONFIRMED)])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 65), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        from infrastructure.models.users import User
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('Please register your email for using your app')
