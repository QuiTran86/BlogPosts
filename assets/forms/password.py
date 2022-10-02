from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from infrastructure.models.users import User


class PasswordResetForm(FlaskForm):

    password = PasswordField('Current Password', validators=[DataRequired()])
    password2 = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User.query.filter_by(email=current_user.email).first()

    def validate_password(self, field):
        if not self.user.verify_password(field.data):
            raise ValidationError('Current password is not correct!')

    def validate_password2(self, field):
        if self.user.verify_password(field.data):
            raise ValidationError('Your new password is equal to the current password.')