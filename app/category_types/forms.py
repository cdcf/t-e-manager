__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CategoryTypeForm(FlaskForm):
    name = StringField('Category Type', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')


class EditCategoryTypeForm(FlaskForm):
    name = StringField('Category Type', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')
