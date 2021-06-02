import datetime
# from telegram import *
# from telegram.ext import *
import urllib.request, urllib.parse
import urllib
from flask import Flask, render_template, redirect, url_for, flash, request, session
from forms import BranchesForm, FeedbackForm, Registration, Delivery, ItemForm, LoginForm, UserForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,current_user,LoginManager, login_required
# from flask_session import Session
import secrets
import os
from pathlib import Path
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://adumatta:0vc.YyvgQIjMHr5d@SG-Cluster1-1945-pgsql-master.servers.mongodirector.com:6432/testdb2?sslmode="require")'
# DATABASE_URI = "postgresql://adumatta:0vc.YyvgQIjMHr5d@SG-Cluster1-1945-pgsql-master.servers.mongodirector.com:6432/testdb2"
# DATABASE_URI = "postgresql://sgpostgres:0vc.YyvgQIjMHr5d@SG-Cluster1-1945-pgsql-master.servers.mongodirector.com:5432/postgres"
DATABASE_URI = "postgresql://sgpostgres:mu6m2uR7V5%40KMuQF@SG-MultiClusterTest-1969-pgsql-master.servers.mongodirector.com:5432/postgres"
# ssl_mode = " sslmode=verify-ca"
# data_folder = Path("ca.pem")
# print(data_folder)
# ssl_root_cert = "&sslrootcert="
# DATABASE_URI += ssl_mode 
# + ssl_root_cert 
# print("CA.PEM file:" + str(data_folder))
# f = open(data_folder)
# print(f.read())

# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
print("DB IS" + DATABASE_URI)
# conn = psycopg2.connect(dbname='testdb2', user='adumatta', password='0vc.YyvgQIjMHr5d', host='SG-Cluster1-1945-pgsql-master.servers.mongodirector.com', port='5432', sslmode='require')
# app.config['SQLALCHEMY_DATABASE_URI'] =  conn
# app.config['SQLALCHEMY_DATABASE_URI'] = 'psycopg2.connect(host="SG-Cluster1-1945-pgsql-master.servers.mongodirector.com" user="adumatta" password="Babebabe123" dbname="testdb2" port=6432)'
db = SQLAlchemy(app)
# session = Session(app)
# SESSION_TYPE = 'filesystem'
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
migrate = Migrate(app, db)
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


# bot = Bot("1699472650:AAEso9qTbz1ODvKZMgRru5FhCEux_91bgK0")
# updater = Updater("1699472650:AAEso9qTbz1ODvKZMgRru5FhCEux_91bgK0", use_context=True)
# dispatcher = updater.dispatcher

# def test_function(update:Update,context:CallbackContext):
#     bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Charley, be like my bot dey workkkkk",
#     )


# start_value=CommandHandler('testone',test_function)
# dispatcher.add_handler(start_value)


# updater.start_polling()


# texxt = "Try this here"


# urlll = "https://api.telegram.org/bot1699472650:AAEso9qTbz1ODvKZMgRru5FhCEux_91bgK0/sendMessage?chat_id=-573994352&text=" + texxt
# print(urlll)

@app.route('/')
def index():
    return render_template('landingpage.html', title = 'Basillisa')

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out.','danger')
    return redirect(url_for("index"))

# params = {"key":api_key,"to":phone,"msg":message,"sender_id":sender_id}
    # url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    # content = urllib.request.urlopen(url).read()

@app.errorhandler(404)
def error_404(error):
    x = datetime.now()
    today = x.strftime("%Y/%m/%d")
    time = x.strftime("%H:%M:%S")
    params = "404\n" + request.url + '\n' + today + " " + time + '\n' + "You can check your logs here https://dashboard.heroku.com/apps/basilissa/logs"
    print("texxt")
    print(request.url)
    print(params)
    url = "https://api.telegram.org/bot1699472650:AAEso9qTbz1ODvKZMgRru5FhCEux_91bgK0/sendMessage?chat_id=-573994352&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(today)
    print(time)
    # print(content)
    # print(url)
    # token = "1699472650:AAEso9qTbz1ODvKZMgRru5FhCEux_91bgK0"
    # chat_id = "-573994352"
    return render_template('404.html', error=error),404

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
    if request.method == 'GET':
        print("Get")

    if request.method == 'POST':
        print('It is a post method')
        print(current_user)
        if current_user.is_authenticated:
            form.name.data = current_user.name
            form.phone.data = current_user.phone
            form.branch.data = branch
            form.items = cart
        else:
            form.branch.data = branch
            print("Not Logged in Yet")
           
        
    if form.validate_on_submit():
        order = Order(order = cart, user = form.name.data, phone = form.phone.data, location = form.location.data, branch = form.branch.data, total=form.total.data )
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
        send_sms(phone,message)
        return redirect(url_for('reciept', id=orderId))
    return render_template('delivery.html', form=form) 


@app.route('/user', methods=['POST','GET'])
def viewuser():
    form = UserForm()
    user = User.query.filter_by(id = current_user.id).first()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    if request.method == 'POST':
        if form.validate_on_submit:
            user.name = form.name.data
            user.email = form.email.data
            user.phone = form.phone.data
            User(name = form.name.data,email = form.email.data, phone = form.phone.data,  )
            db.session.commit()
            print("EII")
            return redirect(url_for("account"))
    return render_template('viewuser.html', user=user, form=form)


@app.route('/feedback', methods=['POST','GET'])
def feedback():
    form = FeedbackForm()
    if request.method == 'GET':
        print('Its a get request now.')
    if form.validate_on_submit():
        feedback = Feedback(name = form.name.data, phone = form.phone.data, description = form.feedback.data )
        send_sms("0545977791","New Feedback")
        db.session.add(feedback)
        db.session.commit()
        print('done')
        flash(f'Thank you for your feedback','success')
    return render_template('feedback.html', form=form)



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
        # send_sms(api_key,phone,message,sender_id)

    return render_template('delivery.html', form=form)

@app.route('/account/orders')
def accountorders():
    print(current_user)
    orders = Order.query.filter_by(user = current_user.name).all()
    print(orders)
    return render_template('accountorders.html', orders=orders)

@app.route('/maps', methods=['GET','POST'])
def maps():
    form = BranchesForm()
    if form.validate_on_submit():
        print(form.location.data)
        return redirect(url_for('menu', location=form.branch.data))
    return render_template('maps copy.html', form=form)

@app.route('/addrider')
def addrider():
    return render_template('add-rider.html', title='Riders')

@app.route('/account')
def account():
    user = current_user
    return render_template('account.html', user=user)

@app.route('/dashboard')
def dashboard():
    inventory = Item.query.all()
    inventoryTotal = len(inventory)
    users = User.query.all()
    totalUsers = len(users)
    print(totalUsers)
    # riders = Riders.query.all()
    # ridersTotal = len(riders)
    return render_template('dash-dashboard.html', inventory = inventoryTotal, title='Dashboard', users=totalUsers)

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

@app.route('/dash-feedback')
def dashfeedback():
    allfeedback = Feedback.query.all()
    return render_template('dash-feedback.html', title='Feedback',allfeedback=allfeedback)


@app.route('/signup', methods=['POST','GET'])
def signup():
    form = Registration()
    if form.validate_on_submit():
        print('Success')
        user = User(name = form.name.data, email = form.email.data, phone = form.phone.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        print(current_user)
        flash(f'' + user.name +', your account has been created ', 'success')
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

def send_sms(phone,message):
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH"
    sender_id = "Basilissa"
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
            login_user(user, remember=True)
            flash (f'Login for ' + user.name ,'success')
            return redirect(url_for('index'))
            # next = request.args.get('next')
        else:
            flash (f'The account cant be found', 'danger')
    return render_template('login.html', form=form)


@app.route("/reciept/<int:id>")
def reciept(id):
    print(id)
    order = Order.query.filter_by(id=id).first()
    return render_template('reciept.html', order = order)

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