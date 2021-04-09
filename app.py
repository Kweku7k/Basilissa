import urllib.request, urllib.parse
import urllib
from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import Registration, Delivery, ItemForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,current_user,LoginManager, login_required
# from flask_session import Session

import secrets
import os
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    print ("The picture name is" + picture_fn)

    return picture_fn



@app.route('/')
def index():
    return render_template('landingpage.html', title = 'Basillisa')

@app.route('/menu/<string:location>')
def menu(location):
    print(location)
    session['location'] = location
    return render_template('menu2.html', location=location)

@app.route('/description/<int:id>')
def description(id):
    item = Item.query.filter_by(id=id).first()
    return render_template('description.html', item=item)

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
        return redirect(url_for('reciept'))
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

@app.route('/addrider')
def addrider():
    return render_template('add-rider.html', title='Riders')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/dashboard')
def dashboard():
    inventory = Item.query.all()
    inventoryTotal = len(inventory)
    # riders = Riders.query.all()
    # ridersTotal = len(riders)
    return render_template('dash-dashboard.html', inventory = inventoryTotal, title='Dashboard')

@app.route('/dash-orders')
def dashorders():
    orders = Order.query.all()
    return render_template('dash-orders.html', title='Orders', orders = orders)

@app.route('/dash-inventory')
def dashinventory():
    return render_template('dash-inventory.html', title='Inventory')

@app.route('/dash-inventory/<string:category>')
def viewdashinventory(category):
    print(category)
    items = Item.query.all()
    print(items)
    return render_template('dash-categories.html', title='Inventory', category=category, items=items)

@app.route('/dash-riders')
def dashriders():
    return render_template('dash-riders.html', title='Riders')

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
    return render_template('explore2.html', items = items, itemname=itemname)

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
        pic = 'burger.jpg'
        if form.image.data:
            print('YO!!!!!!!!! IT IS OVER HERE!!!')
            pic= save_picture(form.image.data)
        item = Item(name = form.name.data, price=form.price.data, description=form.description.data, category=form.category.data, image_file = pic)
        flash (f'New Item has been added','success')
        db.session.add(item)
        db.session.commit()
        print(item.image_file)
        return redirect(url_for('viewdashinventory',category=form.category.data))
    return render_template('additem.html', form=form)

@app.route('/item/<int:id>', methods=['POST','GET'])
def item(id):
    form = ItemForm()
    # item = Item.query.filter_by(id = id).first()
    item = Item.query.filter_by(id = id).first()
    print(item.image_file)
    if request.method == 'POST':
        if form.validate_on_submit():
            pic = item.image_file
            print(pic)
            if form.image.data:
                print('There is a picture in the form')
                pic= save_picture(form.image.data)
            print('Form has validated successfully')
            print(form.price.data)
            print(item)
            item.name = form.name.data
            item.price = form.price.data
            item.description = form.description.data
            item.image_file = pic
            db.session.commit()
            print(item.name)
            return redirect(url_for('viewdashinventory',category=form.category.data))
    if request.method == 'GET':
        form.name.data = item.name
        form.price.data = item.price
        form.description.data = item.description
    return render_template('item.html', item=item, form=form)

@app.route('/cart', methods=['POST','GET'])
def cart():
    cart = request.form['cart']
    print(str(cart))
    cartArray =  cart.split(",")
    print("cart array")
    print(len(cartArray))
    items = []
    for x in cartArray:
        print(x)
        item = Item.query.filter_by(id = x).first()
        items.append(item)
        print(item)
    return render_template('cart.html', items = items)


@app.route('/dash')
def dash():
    return render_template('dashboard2.html')

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


@app.route("/reciept")
def reciept():
    return render_template('reciept.html')

@app.route('/items')
def items():
    items = Item.query.all()
    return render_template('items.html', items = items)

@app.route('/delete/<int:id>')
def delete(id):
    print(id)
    item = Item.query.filter_by(id=id).first()
    category = item.category
    # os.remove()
    db.session.delete(item)
    db.session.commit()
    flash('Item has been deleted successfully', 'danger')
    return redirect(url_for('viewdashinventory',category=category))

if __name__ == '__main__':
    app.run(debug=True)