__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from app.models import Client


def get_clients():
    return Client.query


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[Length(min=0, max=128)])
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a client --')
    submit = SubmitField('Save')


class EditProjectForm(FlaskForm):
    name = StringField('Project name', validators=[DataRequired()])
    description = TextAreaField('Project Description', validators=[Length(min=0, max=128)])
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a client --')
    submit = SubmitField('Save')


class ListProjectForm(FlaskForm):
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a client --')
    submit = SubmitField('Search')
