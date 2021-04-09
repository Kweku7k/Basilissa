from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("Password")])
    submit = SubmitField('SignUp')

class Delivery(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    cart = StringField('Cart', validators=[DataRequired()])
    notes = StringField('Notes', widget=TextArea())
    branch = StringField('Branch', validators=[DataRequired()])
    submit = SubmitField('Place Order')

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    image = FileField('Add a picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', choices=[('Pizza', 'Pizza'),('Chineese','Chineese'),('Cocktails','Cocktails'),('Shawarma','Shawarma'),('Chicken','Chicken'),('Rice','Rice')])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
