from flask_wtf import FlaskForm
from wtforms import TextAreaField


class BlogForms(FlaskForm):
    body = TextAreaField()
