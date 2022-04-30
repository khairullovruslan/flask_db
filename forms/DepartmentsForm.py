from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Departments Title', validators=[DataRequired()])
    chief = IntegerField('Team Leader id', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')