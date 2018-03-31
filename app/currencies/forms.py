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

    def validate_name(self, name):
        currency = Currency.query.filter_by(name=name.data).first()
        if currency is not None:
            raise ValidationError('Currency is already registered, please choose another one.')

    def validate_default_curr(self, default_curr):
        if default_curr.data == True:
            currency = Currency.query.filter_by(default_curr=True).first()
            if currency is not None:
                raise ValidationError('Default currency has already been set, you cannot add another default.')


class EditCurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    description = StringField('Currency Name')
    default_curr = BooleanField('')
    submit = SubmitField('Save')

    def __init__(self, original_name, *args, **kwargs):
        super(EditCurrencyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            currency = Currency.query.filter_by(name=self.name.data).first()
            if currency is not None:
                raise ValidationError('Currency already in use, please use a different one.')

    def validate_default_curr(self, default_curr):
        if default_curr.data == True:
            currency = Currency.query.filter_by(default_curr=True).first()
            print(default_curr.data)
            if currency is not None:
                raise ValidationError('Default currency has already been set, you cannot add another default.')
