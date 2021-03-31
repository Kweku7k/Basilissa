from app import db
from flask_login import UserMixin
from datetime import datetime

def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.phone}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(200), default='default.png')
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Item('{self.name}', '{self.price}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(), nullable=False)
    user = db.Column(db.String(),nullable=False)
    phone = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    branch = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Item('{self.id}', '{self.date_created}')"