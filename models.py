from exts import db
from datetime import datetime

class SuppliersModel(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usename = db.Column(db.String(50), nullable=False)
    linkman = db.Column(db.String(30), nullable=False)
    pyone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    
    # ✅ 修正关系名称（确保与 ProductsModel.back_populates 一致）
    products = db.relationship('ProductsModel', back_populates="supplier")

class ProductsModel(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usename = db.Column(db.String(50), nullable=False)
    standard = db.Column(db.String(60), nullable=False)
    unitprice = db.Column(db.String(10), nullable=False)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))  # ✅ 外键字段必须存在
    orders = db.relationship('OrdersModel', back_populates="product")
    # ✅ 修正关系名称（确保与 InventoryModel.back_populates 一致）
    Outproduct_inventory = db.relationship('InventoryModel', back_populates="Outinventory_product")
    # ✅ 修正关系名称（确保与 OrdersModel.back_populates 一致）
    supplier = db.relationship('SuppliersModel', back_populates="products")

class InventoryModel(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # ✅ 修正关系名称（确保与 ProductsModel.back_populates 一致）
    Outinventory_product = db.relationship('ProductsModel', back_populates="Outproduct_inventory")
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
# models.py
class CustomersModel(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usename = db.Column(db.String(50), nullable=False)
    pyone = db.Column(db.String(20), nullable=False)
    
    # ✅ 修正关系名称（确保与 OrdersModel.back_populates 一致）
    orders = db.relationship('OrdersModel', back_populates="customer")
# models.py
# ✅ 正确：create_time 是 DateTime 类型
# ✅ 正确：关系名称完全一致
class OrdersModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    money = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    
    # ✅ 修正关系名称（确保与 CustomersModel.back_populates 一致）
    customer = db.relationship('CustomersModel', back_populates="orders")
    # ✅ 修正关系名称（确保与 ProductsModel.back_populates 一致）
    product = db.relationship('ProductsModel', back_populates="orders")
    
    # ✅ 使用 DateTime 字段
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)  # ✅ 添加唯一性
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)     # ✅ 添加唯一性   
    

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, index=True)  # ✅ 添加索引
    captcha = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)