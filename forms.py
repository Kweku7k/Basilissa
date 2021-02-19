from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Delivery(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Place Order')

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('Add a picture', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField('Category', choices=[('Pizza', 'Pizza'),('Chineese','Chineese'),('Cocktails','Cocktails'),('Shawarma','Shawarma'),('Chicken','Chicken'),('Rice','Rice')])
    submit = SubmitField('Submit')
    
class LoginForm():
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
