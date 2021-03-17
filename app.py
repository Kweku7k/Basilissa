import urllib.request, urllib.parse
import urllib
from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import Registration, Delivery, ItemForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,current_user,LoginManager, login_required
# from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# session = Session(app)
# SESSION_TYPE = 'filesystem'
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('landingpage.html', title = 'Basillisa')

@app.route('/menu/<string:location>')
def menu(location):
    print(location)
    session['location'] = location
    return render_template('menu.html', location=location)

@app.route("/summary", methods=['POST','GET'])
def summary():
    form = Delivery()
    cart = request.form['cart']
    print(cart)
    # print(current_user)
    branch = session['location']
    print(branch)
    if request.method == 'POST':
        print('It is a post method')
        # form.name.data = current_user.name
        # form.phone.data = current_user.phone
        form.branch.data = branch
        form.items = cart
    if form.validate_on_submit():
        order = Order(order = cart, user = form.name.data, phone = form.phone.data, location = form.location.data, branch = form.branch.data )
        db.session.add(order)
        db.session.commit()
        print (order.id)
        orderId = order.id
        orderid = str(orderId)
        api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
        # phone = "‭0249411910‬" #SMS recepient"s phone number
        phone = "0545977791" #SMS recepient"s phone number
        # newrl = (url_for(form.location.data))
        # console.log(newrl)
        message = "You have recieved a new order from " + form.name.data + ". Order id " + orderid + " at " +  form.location.data + ". Check your dashboard for more information &"
        sender_id = "Basilissa" #11 Characters maximum
        send_sms(api_key,phone,message,sender_id)
        return render_template('summary.html', id=orderId)
    return render_template('delivery.html', form=form) 


@app.route('/hoh', methods=['POST','GET'])
def delivery():
    form = Delivery()
    if request.method == 'GET':
        print('It is a post method')
        form.name.data = current_user.name
        form.phone.data = current_user.phone
    if form.validate_on_submit():
        api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
        phone = "0249411910" #SMS recepient"s phone number
        message = "You have recieved a new order. please check your dashboard to confirm."
        sender_id = "Basilissa" #11 Characters maximum
        send_sms(api_key,phone,message,sender_id)

    return render_template('delivery.html', form=form)

@app.route('/maps')
def maps():
    return render_template('maps copy.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/dashboard')
def dashboard():
    tot = Item.query.all()
    total = len(tot)
    return render_template('dashboard.html', total=total)

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
    location = session['location']
    print(location)
    return render_template('explore.html', items=items)

@app.route('/branches')
def branches():
    return render_template('branches.html')

@app.route('/riders')
def riders():
    return render_template('riders.html')

@app.route('/additem', methods=['POST','GET'])
def additem():
    form = ItemForm()
    if form.validate_on_submit():
        flash (f'New Item has been added','success')
        item = Item(name = form.name.data, price=form.price.data, description=form.description.data, category=form.category.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('items'))
    return render_template('additem.html', form=form)

@app.route('/item/<int:id>', methods=['POST','GET'])
def item(id):
    form = ItemForm()
    item = Item.query.filter_by(id=id).first()
    if request.method == 'GET':
        form.name.data = item.name
        form.price.data = item.price
        form.description.data = item.description
    if request.method == 'POST':
        newitem = Item(name = form.name.data, price=form.price.data, description = form.description.data)
        db.session.commit()
        return redirect(url_for('items'))
    return render_template('item.html', item=item, form=form)

@app.route('/cart')
def cart():
    return render_template('cart.html')


def send_sms(api_key,phone,message,sender_id):
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print (content)
    print (url)

@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:id>')
def order(id):
    order = Order.query.filter_by(id=id).first()
    print(order)
    return render_template('order.html', order=order)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    items = []
    new = []
    piw = projectpath.replace(',', '')
    print ("final " + piw)
    #  Shows the items in the cart
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
            login_user(user)
            flash (f'Login for ' + user.name ,'success')
            return redirect(url_for('index'))
            # next = request.args.get('next')
        else:
            flash (f'The account cant be found', 'danger')
    return render_template('login.html', form=form)


@app.route('/items')
def items():
    items = Item.query.all()
    return render_template('items.html', items = items)

@app.route('/delete/<int:id>')
def delete(id):
    print(id)
    item = Item.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect('/items')

if __name__ == '__main__':
    app.run(debug=True)