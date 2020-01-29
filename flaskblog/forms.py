from flask_wtf import FlaskForm
from flask_login import current_user

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import User







class RegistrationForm(FlaskForm):

    username = StringField('Username',

                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',

                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',

                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')





class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    
    title=StringField('Title',validators=[DataRequired()])
    
    content=TextAreaField('content',validators=[DataRequired()])
    
    submit=SubmitField('post')

class AboutForm(FlaskForm):

    name = StringField('name',

                        validators=[DataRequired()])

    description=TextAreaField('description',validators=[DataRequired()])


    submit = SubmitField('Add information')
