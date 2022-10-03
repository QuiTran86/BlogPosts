from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from infrastructure.models.users import User


class PasswordResetForm(FlaskForm):
    MESSAGE_NEW_PASSWORD_CONFIRMED = 'Should match to desired password.'

    password = PasswordField('Current Password', validators=[DataRequired()])
    password1 = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password',
                              validators=[DataRequired(), EqualTo('password1',
                                                                  message=MESSAGE_NEW_PASSWORD_CONFIRMED)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User.query.filter_by(email=current_user.email).first()

    def validate_password(self, field):
        if not self.user.verify_password(field.data):
            raise ValidationError('Current password is not correct!')
