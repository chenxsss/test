from exts import db
from datetime import datetime

class SuppliersModel(db.Mpdel):
    __tablename__ = 'suppliers'
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    usename = db.Column(db.String(50),nullable=False)
    linkman = db.Column(db.String(30),nullable=False)
    pyone = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(50),nullable=False)
    Outsupply_products = db.relationship('ProductsModel',back_populates='Outproduct_supply')

class ProductsModel(db.Model):
    __tablename__ = 'products'
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    usename = db.Column(db.String(50),nullable=False)
    standard = db.Column(db.String(60),nullable = False)
    unitprice = db.Column(db.String(10),nullable=False)
    Outproduct_supply = db.relationship('SuppliersModel',back_populates = "Outsupply_products")
    Outproduct_inventory= db.relationship('InventoryModel',back_populates = "Outinventory_product")
    Outproducts_order = db.relationship('OrdersModel', back_populates="Outorder_prodect")

class InventoryModel(db.Model):
    __tablename__ = 'inventory'
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    quantity = db.Column(db.Integer, nullable=False)
    Outinventory_product = db.relationship('ProductsModel',back_populates = "Outproduct_inventory")
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


class CustomersModel(db.Model):
    __tablename__ = 'customers'
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    usename = db.Column(db.String(50),nullable=False)
    pyone = db.Column(db.String(20),nullable=False)
    Outcustomer_order = db.relationship('OrdersModel',back_populates = "Outorder_customer")
    
class OrdersModel(db.Model):
    __tablename__ = 'orders'
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    type = db.Column(db.String(20),nullable=False)
    money = db.Column(db.String(20),nullable = False)
    status = db.Column(db.String(20),nullable=False)
    Outcustomer = db.Column(db.Integer,db.ForeignKey('customers.id'))
    Outorder_products= db.relationship('ProductsModel',back_populates = "Outproducts_order")


class UserModel(db.Model):
    __tablename__ = "user"
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    username = db.Column(db.String(100),nullable =False)
    password = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(100),nullable = False,unique = True)
    

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id =db.Column(db.Integer,primary_key=True,autoincrement = True)
    email = db.Column(db.String(100),nullable = False,unique = True)
    captcha = db.Column(db.String(20),nullable = False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)