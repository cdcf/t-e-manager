__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DecimalField, DateField, HiddenField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Category, CategoryType, Currency, Client, Project
import datetime


def get_categories():
    return Category.query


def get_category_types():
    return CategoryType.query


def get_clients():
    return Client.query


def get_projects():
    return Project.query


def get_currencies():
    return Currency.query


def get_default_currency():
    return Currency.query.filter_by(default_curr=True).first()


class ExpenseForm(FlaskForm):
    form_name = HiddenField('Form Name')
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    name = StringField('Expense Description', validators=[DataRequired()])
    location = StringField('Location')
    category_id = QuerySelectField('Expense Category', validators=[DataRequired()],
                                   query_factory=get_categories,
                                   allow_blank=True,
                                   get_label='name',
                                   blank_text=u'-- Please choose a category --',
                                   id='select_category')
    category_type_id = QuerySelectField('Category Type', validators=[DataRequired()],
                                        query_factory=get_category_types,
                                        allow_blank=True,
                                        get_label='name',
                                        blank_text=u'-- Please choose a category type --',
                                        id='select_category_type')
    amount = DecimalField('Amount')
    currency_id = QuerySelectField('Currency', validators=[DataRequired()],
                                   query_factory=get_currencies,
                                   allow_blank=True,
                                   get_label='name',
                                   default=get_default_currency)
    guest = BooleanField('Add guest')
    guest_list = StringField('Guests')
    scan = StringField('Scan')
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
    submit = SubmitField('Save')


class EditExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%d/%m/%Y', default=datetime.date.today(),
                     id='date_picker')
    name = StringField('Category Type', validators=[DataRequired()])
    location = StringField('Location')
    category_id = QuerySelectField('Expense Category', validators=[DataRequired()],
                                   query_factory=get_categories,
                                   allow_blank=True,
                                   get_label='name',
                                   blank_text=u'-- Please choose an expense category --',
                                   id='select_category')
    category_type_id = QuerySelectField('Category Type', validators=[DataRequired()],
                                        query_factory=get_category_types,
                                        allow_blank=True,
                                        get_label='name',
                                        blank_text=u'-- Please choose a category type --',
                                        id='select_category_type')
    amount = DecimalField('Amount')
    currency_id = QuerySelectField('Currency', validators=[DataRequired()],
                                query_factory=get_currencies,
                                allow_blank=True,
                                get_label='name')
    guest = BooleanField('Add guest')
    guest_list = StringField('Guests')
    scan = StringField('Scan')
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
    form_name = HiddenField('Form Name')
    submit = SubmitField('Save')


class ListExpenseForm(FlaskForm):
    date_from = DateField('Date From', validators=[DataRequired()], format='%d/%m/%Y', id='from_date_picker')
    date_to = DateField('Date To', validators=[DataRequired()], format='%d/%m/%Y', id='to_date_picker')
    category_id = QuerySelectField('Expense Category', validators=[DataRequired()],
                                   query_factory=get_categories,
                                   allow_blank=True,
                                   get_label='name',
                                   blank_text=u'-- Please choose an expense category --')
    category_type_id = QuerySelectField('Category Type', validators=[DataRequired()],
                                        query_factory=get_category_types,
                                        allow_blank=True,
                                        get_label='name',
                                        blank_text=u'-- Please choose a category type --')
    client_id = QuerySelectField('Client', validators=[DataRequired()],
                                 query_factory=get_clients,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a client --')
    project_id = QuerySelectField('Project', validators=[DataRequired()],
                                  query_factory=get_projects,
                                  allow_blank=True,
                                  get_label='name',
                                  blank_text=u'-- Please choose a project --')
    submit = SubmitField('Search')
