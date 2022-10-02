from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')
