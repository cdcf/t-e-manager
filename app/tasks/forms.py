__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, DateField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from app.models import Client, Project, Currency
import datetime


def get_clients():
    return Client.query


def get_projects():
    return Project.query


def get_currencies():
    return Currency.query


def get_default_currency():
    return Currency.query.filter_by(default_curr=True).first()



class TaskForm(FlaskForm):
    form_name = HiddenField('Form Name')
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
                                  id='select_project')
    task_ref = StringField('Task Ref', validators=[DataRequired()])
    duration = DecimalField('Duration', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    rate = DecimalField('Rate', validators=[DataRequired()])
    currency_id = QuerySelectField('Currency', validators=[DataRequired()],
                                   query_factory=get_currencies,
                                   allow_blank=True,
                                   get_label='name',
                                   default=get_default_currency)
    comment = TextAreaField('Comments', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')


class EditTaskForm(FlaskForm):
    form_name = HiddenField('Form Name')
    name = StringField('Task Description', validators=[DataRequired()])
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a project --',
                                 id='select_client')
    project_id = QuerySelectField('Project', validators=[DataRequired()],
                                  query_factory=get_projects,
                                  allow_blank=True,
                                  get_label='name',
                                  id='select_project')
    task_ref = StringField('Task Ref', validators=[DataRequired()])
    duration = DecimalField('Duration', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', id='date_picker')
    rate = DecimalField('Rate', validators=[DataRequired()])
    currency_id = QuerySelectField('Currency', validators=[DataRequired()],
                                   query_factory=get_currencies,
                                   allow_blank=True,
                                   get_label='name')
    comment = TextAreaField('Comments', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')


class ListTaskForm(FlaskForm):
    date_from = DateField('Date From', validators=[DataRequired()], format='%d/%m/%Y', id='from_date_picker')
    date_to = DateField('Date To', validators=[DataRequired()], format='%d/%m/%Y', id='to_date_picker')
    submit = SubmitField('Search')
