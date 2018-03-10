__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[Length(min=0, max=128)])
    submit = SubmitField('Save')


class EditProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[Length(min=0, max=128)])
    submit = SubmitField('Save')
