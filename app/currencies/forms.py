__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from app.models import Currency


class CurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    default = BooleanField('Default currency')
    submit = SubmitField('Save')

    def __init__(self, original_name, original_default, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_default = original_default

    def validate_name(self, name):
        if name.data != self.original_name:
            currency = Currency.query.filter_by(name=self.name.data).first()
            if currency is not None:
                raise ValidationError('Currency already in use, please use a different one.')

    def validate_default(self, default):
        if default.data != self.original_default:
            currency = Currency.query.filter_by(default=self.default.data).first()
            if currency is not None:
                raise ValidationError('A default currency has already been set, you cannot make this one as default.')


class EditCurrencyForm(FlaskForm):
    name = StringField('Currency', validators=[DataRequired()])
    default = BooleanField('Default currency')
    submit = SubmitField('Save')

    def __init__(self, original_name, original_default, *args, **kwargs):
        super(EditCurrencyForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_default = original_default

    def validate_name(self, name):
        if name.data != self.original_name:
            currency = Currency.query.filter_by(name=self.name.data).first()
            if currency is not None:
                raise ValidationError('Currency already in use, please use a different one.')

    def validate_default(self, default):
        if default.data != self.original_default:
            currency = Currency.query.filter_by(default=self.default.data).first()
            if currency is not None:
                raise ValidationError('A default currency has already been set, you cannot make this one as default.')
