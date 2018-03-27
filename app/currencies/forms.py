__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.models import Currency


class CurrencyForm(FlaskForm):
    name = StringField('Currency Code', validators=[DataRequired()])
    description = StringField('Currency Name')
    default_curr = BooleanField('')
    submit = SubmitField('Save')

    def validate_default_curr(self, default_curr):
        currency = Currency.query.filter(default_curr.data==True).first()
        if currency is not None:
            raise ValidationError('Default currency has already been set, you cannot add another default.')


class EditCurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    description = StringField('Currency Name')
    default_curr = BooleanField('')
    submit = SubmitField('Save')

    def validate_default_curr(self, default_curr):
        currency = Currency.query.filter(default_curr.data==True).first()
        if currency is not None:
            raise ValidationError('Default currency has already been set, you cannot add another default.')
