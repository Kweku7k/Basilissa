from flask import Flask, render_template, redirect, url_for, flash, request
from forms import Registration, Delivery, ItemForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,current_user,LoginManager
import urllib.request, urllib.parse
import urllib

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
from models import *

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', title = 'Basillisa')

@app.route('/menu/<string:location>')
def menu(location):
    print(location)
    return render_template('menu.html', location=location)

@app.route("/summary", methods=['POST','GET'])
def summary():
    cart = request.form['cart']
    print(cart)
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    phone = "0545977791" #SMS recepient"s phone number
    message = "You have recieved a new order. please check your dashboard to confirm."
    sender_id = "Basilissa" #11 Characters maximum
    send_sms(api_key,phone,message,sender_id)
    return render_template('summary.html') 


@app.route('/delivery', methods=['POST','GET'])
def delivery():
    form = Delivery()
    if request.method == 'GET':
        print('It is a post method')
        form.name.data = current_user.name
        form.phone.data = current_user.phone
    if form.validate_on_submit():
        api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
        phone = "0545977791" #SMS recepient"s phone number
        message = "You have recieved a new order. please check your dashboard to confirm."
        sender_id = "Basilissa" #11 Characters maximum
        send_sms(api_key,phone,message,sender_id)

    return render_template('delivery.html', form=form)

@app.route('/maps')
def maps():
    return render_template('maps copy.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    form = Registration()
    if form.validate_on_submit():
        print('Success')
        user = User(name = form.name.data, email = form.email.data, phone = form.phone.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print(current_user)
        flash(f'User ' + user.name +' has been created ', 'success')
        return redirect(url_for('index'))
    else:
        print('yawa')
    return render_template('signup.html', form=form)

@app.route('/explore/<string:itemname>')
def explore(itemname):
    items = Item.query.filter_by(category="Pizza").all()
    print(itemname)
    print(items)
    return render_template('explore.html', items=items)

@app.route('/branches')
def branches():
    return render_template('branches.html')

@app.route('/additem', methods=['POST','GET'])
def additem():
    form = ItemForm()
    if form.validate_on_submit():
        flash (f'New Item has been added','success')
        item = Item(name = form.name.data, price=form.price.data, description=form.description.data, category=form.category.data)
        db.session.add(item)
        db.session.commit()
        return('Success')
    return render_template('additem.html', form=form)

@app.route('/allitems')
def allitems():
    items = Item.query.all()
    return render_template('allitems.html', items=items)

@app.route('/cart')
def cart():
    return render_template('cart.html')


def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    items = []
    new = []
    piw = projectpath.replace(',', '')
    print ("final " + piw)
    for x in piw:
        x = int(x)
        item = Item.query.filter_by(id = x).first()
        items.append(item)
        print(item)
        print (x)
        new.append(x)
    print(new)
    return render_template('cart.html', items = items)
    

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash (f'Login for ' + current_user.name ,'success')
            return redirect(url_for('index'))
            
        else:
            flash (f'The account cant be found', 'danger')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)