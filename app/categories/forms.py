__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import Category


class CategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')

    def validate_category(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError('Category is already registered, please choose another one.')


class EditCategoryForm(FlaskForm):
    name = StringField('Category', validators=[DataRequired()])
    colour = StringField('Set a colour')
    submit = SubmitField('Save')

    def validate_category(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError('Category is already registered, please choose another one.')
