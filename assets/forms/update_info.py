from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 63)])
    location = StringField('Location', validators=[Length(0, 63)])
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')
