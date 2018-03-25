__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class CurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    default = BooleanField('Default currency')
    submit = SubmitField('Save')


class EditCurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    default = BooleanField('Default currency')
    submit = SubmitField('Save')
