from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64), index=False, unique=False)
    password_hash = db.Column(db.String(128))
    is_administrator = db.Column(db.String(32), index=False, unique=False)

    def __repr__(self):
        return '<User {}>, {} '.format(self.username, self.is_administrator)

    def update_details(self, username, name, email):
        self.username = username
        self.email = email
        self.name = name
        print(self)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        if self.is_administrator == "Administrator":
            #print("{} is an Administrator".format(self.username))
            return True
        else:
            #print("{} is a Regular User".format(self.username))
            return False


@login.user_loader
def load_user(id):
    #print(User.query.get(int(id)))
    return User.query.get(int(id))


class Product(db.Model):
    productID = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(128), index=False, unique=False)
    purchasePrice = db.Column(db.Float(), index=False, unique=False)
    sellingPrice = db.Column(db.Float(), index=False, unique=False)
    quantity = db.Column(db.Integer, index=False, unique=False)
    image = db.Column(db.String(64), index=False, unique=False)

    def __repr__(self):
        return '<Product {}: {}>'.format(self.id, self.productname)


class Order(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, db.ForeignKey('product.productID'))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    orderdate = db.Column(db.DateTime, index=False, unique=False)

    def __init__(self, userid, productid, order_date=datetime.today()):
        self.userID = userid
        self.productID = productid
        self.orderdate = order_date


    # def __init__(self, userid, productid):
    #     self.userID = userid
    #     self.productID = productid
    #     #self.orderdate = datetime.today()


    def __repr__(self):
        return '<Order {}: User {} Ordered Product {}, date: {}>'.format(self.orderID, self.userID, self.productID, self.orderdate)

