__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from app.models import Client, Project
import datetime


def get_clients():
    return Client.query


def get_projects():
    return Project.query


class TaskForm(FlaskForm):
    name = StringField('Task Description', validators=[DataRequired()])
    client_id = QuerySelectField('Client', validators=[DataRequired()],
        query_factory=get_clients,
        allow_blank=True,
        get_label='name',
        blank_text=u'-- Please choose a client --',
        id='select_client')
    project_id = QuerySelectField('Project', validators=[DataRequired()],
        query_factory=get_projects,
        allow_blank=True,
        get_label='name',
        blank_text=u'-- Please choose a project --',
        id='select_project')
    jira = StringField('Jira Ref', validators=[DataRequired()])
    duration = DecimalField('Duration', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    rate = DecimalField('Rate', validators=[DataRequired()])
    comment = TextAreaField('Comments', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')


class EditTaskForm(FlaskForm):
    name = StringField('Task Description', validators=[DataRequired()])
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name')
    project_id = QuerySelectField('Project', validators=[DataRequired()],
                                  query_factory=get_projects,
                                  allow_blank=True,
                                  get_label='name')
    jira = StringField('Jira Ref', validators=[DataRequired()])
    duration = DecimalField('Duration', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', id='date_picker')
    rate = DecimalField('Rate', validators=[DataRequired()])
    comment = TextAreaField('Comments', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')


class ListTaskForm(FlaskForm):
    date_from = DateField('Date From', validators=[DataRequired()], format='%d/%m/%Y', id='from_date_picker')
    date_to = DateField('Date To', validators=[DataRequired()], format='%d/%m/%Y', id='to_date_picker')
    submit = SubmitField('Search')
