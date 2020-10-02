from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
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

    # validate_field(self,field)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        print(user)
        if user:
            raise ValidationError("this username is already taken! please choose another one!")

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        print(user_email)
        if user_email:
            raise ValidationError("this email is already taken! please choose another one!")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # validate_field(self,field)
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # print(user)
            if user:
                raise ValidationError("this username is already taken! please choose another one!")

    def validate_email(self, email):
        if email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            # print(user_email)
            if user_email:
                raise ValidationError("this email is already taken! please choose another one!")



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        print(user_email)
        if user_email is None:
            raise ValidationError("there is no account with that Email. you must register first")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')