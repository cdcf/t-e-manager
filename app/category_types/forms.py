__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import CategoryType, Category


def get_category():
    return Category.query


class CategoryTypeForm(FlaskForm):
    category_id = QuerySelectField('Category', validators=[DataRequired()],
                                 query_factory=get_category,
                                 allow_blank=True,
                                 get_label='name',
                                 blank_text=u'-- Please choose a category --')
    name = StringField('Category Type', validators=[DataRequired()])
    icon = StringField('Set an icon')
    submit = SubmitField('Save')

    def validate_name(self, name):
        category_type = CategoryType.query.filter_by(name=name.data).first()
        if category_type is not None:
            raise ValidationError('Category Type is already registered, please choose another one.')


class EditCategoryTypeForm(FlaskForm):
    category_id = QuerySelectField('Category', validators=[DataRequired()],
                                   query_factory=get_category,
                                   allow_blank=True,
                                   get_label='name',
                                   blank_text=u'-- Please choose a category --')
    name = StringField('Category Type', validators=[DataRequired()])
    icon = StringField('Set an icon')
    submit = SubmitField('Save')

    def __init__(self, original_name, *args, **kwargs):
        super(EditCategoryTypeForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        category_type = CategoryType.query.filter_by(name=name.data).first()
        if category_type is not None:
            raise ValidationError('Category Type is already registered, please choose another one.')
