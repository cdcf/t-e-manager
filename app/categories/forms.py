__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')


class EditCategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')
