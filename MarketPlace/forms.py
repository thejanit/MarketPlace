from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from MarketPlace.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username= username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try different username')

    def validate_email_add(self, email_add_to_check):
        email_add = User.query.filter_by(email_add= email_add_to_check.data).first()
        if email_add:
            raise ValidationError('Email Address already exist! Please try different email address')

    username = StringField(label='User Name', validators=[Length(min=2, max=10), DataRequired()])
    email_add = StringField(label='Email Address', validators=[Email(), DataRequired()])
    passwd1  = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    passwd2 = PasswordField(label='Confirm Password', validators=[EqualTo('passwd1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    passwd = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class BuyingItemForm(FlaskForm):
    submit = SubmitField(label='Buy Item')


class SellingItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')

