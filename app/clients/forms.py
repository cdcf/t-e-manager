__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ClientForm(FlaskForm):
    name = StringField('Client name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Length(min=0, max=128)])
    submit = SubmitField('Save')


class EditClientForm(FlaskForm):
    name = StringField('Client name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Length(min=0, max=128)])
    submit = SubmitField('Save')
