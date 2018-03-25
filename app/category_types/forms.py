__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import CategoryType


class CategoryTypeForm(FlaskForm):
    name = StringField('Category Type', validators=[DataRequired()])
    icon = StringField('Set an icon')
    submit = SubmitField('Save')

    def validate_category_type(self, name):
        category_type = CategoryType.query.filter_by(name=name.data).first()
        if category_type is not None:
            raise ValidationError('Category Type is already registered, please choose another one.')


class EditCategoryTypeForm(FlaskForm):
    name = StringField('Category Type', validators=[DataRequired()])
    icon = StringField('Set an icon')
    submit = SubmitField('Save')

    def validate_category_type(self, name):
        category_type = CategoryType.query.filter_by(name=name.data).first()
        if category_type is not None:
            raise ValidationError('Category Type is already registered, please choose another one.')
