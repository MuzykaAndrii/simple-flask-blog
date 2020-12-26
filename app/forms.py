from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25, 
                            message='Username length must be in range from 4 to 25 characters'),
                            DataRequired(message='This area is required'), Regexp('[A-Za-z][A-Za-z0-9_.]*$', 0, 'Unexpected charachter in username')])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[Length(min=6, 
                            message='Password should be bigger than 6 characters'), 
                            DataRequired(message='This area is required')])

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(message='This area is required'), 
                            EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25, 
                            message='Username length must be in range from 4 to 25 characters'),
                            DataRequired(message='This area is required'), Regexp('[A-Za-z][A-Za-z0-9_.]*$', 0, 'Unexpected charachter in username')])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile picture', validators=[FileAllowed(['jpg', 'png'])])

    about_me = StringField('About me', validators=[Length(min=0, max=300, message='Too long text')])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            result = User.query.filter_by(username=username.data).first()
            if result:
                raise ValidationError('That username already taken, please choose another')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            result = User.query.filter_by(username=email.data).first()
            if result:
                raise ValidationError('That email already taken, please choose another')

class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])

    new_password = PasswordField('New password', validators=[Length(min=6, 
                            message='Password should be bigger than 6 characters'), 
                            DataRequired(message='This area is required')])

    confirm_password = PasswordField('Repeat new Password',
                            validators=[DataRequired(message='This area is required'), 
                            EqualTo('new_password')])
    
    submit = SubmitField('Change password')

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=50, message='Name of post is too short/big')])
    content = CKEditorField('Post text', validators=[DataRequired(), Length(max=10000, message='Text is too big')])
    submit = SubmitField('Submit')