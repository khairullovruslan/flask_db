from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    team_lider = IntegerField("Team Leader id")
    work_size = IntegerField("Work Size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')