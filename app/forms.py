from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    '''
    Description:
        This Class configures the fields that is going to be used to login the user.
        This code is called from within routes.py
    Inputs:
        FlaskForm: passed automatically when called from routes.
    Outputs:
        None
    '''

    # Set up the fields to display on screen
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Emails', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class OrderForm(FlaskForm):
    '''
    Old version of the order form.
    '''
    #userID = StringField('User ID', validators=[DataRequired()])
    productID = StringField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Order')

class ProductOrderForm(FlaskForm):
    checkbox = BooleanField('Item')
    submit = SubmitField('Submit')


class ProductRegistrationForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    purchase_price = FloatField('Purchase price', validators=[DataRequired()])
    selling_price = FloatField('Selling price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image = FileField('Image File Upload', validators=[FileRequired()])
    submit = SubmitField('Register')

class ResetPasswordForm(FlaskForm):
    new_password = StringField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update User Details')


