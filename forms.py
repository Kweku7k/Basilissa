from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email')
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('SignUp')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email')
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update')


class Delivery(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    cart = StringField('Cart', validators=[DataRequired()])
    notes = StringField('Notes', widget=TextArea())
    branch = StringField('Branch', validators=[DataRequired()])
    total = StringField('Total')
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

class BranchesForm(FlaskForm):
    branch = SelectField('Branches', choices=[('Dansoman', 'Dansoman'),('Labone','Labone'),('Afienya','Afienya'),('Dawhenya','Dawhenya'),('Tema','Tema'),('Accra Mall','Accra Mall'),('West Hills Mall','West Hills Mall'),('Achimota Mall','Achimota Mall')])
    location = StringField('Your Location', validators=[DataRequired()])

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    feedback = StringField('Feedback', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Login')
