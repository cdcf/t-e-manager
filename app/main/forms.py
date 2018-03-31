__author__ = 'Cedric Da Costa Faro'

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Role


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already in use, please use a different one.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Email address already in use, please use a different one.')


def get_roles():
    return Role.query


class EditProfileAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    role = QuerySelectField('Role', validators=[DataRequired()],
        query_factory=get_roles,
        allow_blank=True,
        get_label='name',
        blank_text=u'-- Please choose a project --')
    submit = SubmitField('Save')

    def __init__(self, user, original_username, original_email, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already in use, please use a different one.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Email address already in use, please use a different one.')
