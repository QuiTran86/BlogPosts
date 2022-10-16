from flask_wtf import FlaskForm
from wtforms.fields import FileField, SubmitField


class AvatarUpdatedForm(FlaskForm):

    file = FileField('Load Avatar')
    submit = SubmitField('Submit')
