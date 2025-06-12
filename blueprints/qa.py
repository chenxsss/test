from flask import Blueprint,jsonify,url_for,session,g,flash
from flask import render_template,redirect,request
from exts import mail,db
from decorators import login_required
from flask_mail import Message
from forms import OrderForm, SupplierForm, ProductForm, CustomerForm
from models import SuppliersModel,ProductsModel,CustomersModel,OrdersModel,InventoryModel


# 创建蓝图（已包含 /qa 前缀）
bp = Blueprint("qa", __name__, url_prefix="/qa")

# ✅ 供应商管理路由
@bp.route("/suppliers")
@login_required
def suppliers():
    suppliers = SuppliersModel.query.order_by(SuppliersModel.id.desc()).limit(5).all()
    form = SupplierForm()  # ✅ 初始化空表单
    return render_template("suppliers.html", suppliers=suppliers, form=form)

@bp.route("/suppliers/add", methods=['POST'])
@login_required
def add_supplier():
    form = SupplierForm(request.form)
    if form.validate():
        new_supplier = SuppliersModel(
            usename=form.usename.data,
            linkman=form.linkman.data,
            pyone=form.pyone.data,
            address=form.address.data
        )
        db.session.add(new_supplier)
        db.session.commit()
        flash("供应商添加成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.suppliers'))

@bp.route("/suppliers/edit/<int:supplier_id>", methods=['POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = SuppliersModel.query.get_or_404(supplier_id)
    form = SupplierForm(request.form, obj=supplier)
    if form.validate_on_submit():
        form.populate_obj(supplier)
        db.session.commit()
        flash("供应商信息更新成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.suppliers'))

@bp.route("/suppliers/delete/<int:supplier_id>")
@login_required
def delete_supplier(supplier_id):
    supplier = SuppliersModel.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash("供应商删除成功", 'success')
    return redirect(url_for('qa.suppliers'))

# ✅ 产品管理
@bp.route("/products")
@login_required
def products():
    products = ProductsModel.query.all()
    suppliers = SuppliersModel.query.all()
    form = ProductForm()
    return render_template("products.html", products=products, suppliers=suppliers, form=form)

@bp.route("/products/add", methods=['POST'])
@login_required
def add_product():
    form = ProductForm(request.form)
    form.supplier_id.choices = [(s.id, s.usename) for s in SuppliersModel.query.all()]
    
    if form.validate_on_submit():
        new_product = ProductsModel(
            usename=form.usename.data,
            standard=form.standard.data,
            unitprice=form.unitprice.data,
            supplier_id=form.supplier_id.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("产品添加成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.products'))

@bp.route("/products/edit/<int:product_id>", methods=['POST'])
@login_required
def edit_product(product_id):
    product = ProductsModel.query.get_or_404(product_id)
    form = ProductForm(request.form, obj=product)
    form.supplier_id.choices = [(s.id, s.usename) for s in SuppliersModel.query.all()]
    
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash("产品信息更新成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.products'))

@bp.route("/products/delete/<int:product_id>")
@login_required
def delete_product(product_id):
    product = ProductsModel.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("产品删除成功", 'success')
    return redirect(url_for('qa.products'))

@bp.route("/customers")
@login_required
def customers():
    customers = CustomersModel.query.all()
    form = CustomerForm()
    return render_template("customers.html", customers=customers, form=form)

@bp.route("/customers/add", methods=['POST'])
@login_required
def add_customer():
    form = CustomerForm(request.form)
    if form.validate_on_submit():
        new_customer = CustomersModel(
            usename=form.usename.data,
            pyone=form.pyone.data
        )
        db.session.add(new_customer)
        db.session.commit()
        flash("客户添加成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.customers'))

@bp.route("/customers/edit/<int:customer_id>", methods=['POST'])
@login_required
def edit_customer(customer_id):
    customer = CustomersModel.query.get_or_404(customer_id)
    form = CustomerForm(request.form, obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        flash("客户信息更新成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.customers'))

@bp.route("/customers/delete/<int:customer_id>")
@login_required
def delete_customer(customer_id):
    customer = CustomersModel.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("客户删除成功", 'success')
    return redirect(url_for('qa.customers'))


# ✅ 库存管理（需补充库存页面和路由）
@bp.route("/inventory")
@login_required

def inventory():
    # ✅ 正确：create_time 是 DateTime 类型
    recent_orders = OrdersModel.query.order_by(OrdersModel.id.desc()).limit(5).all()
    products = ProductsModel.query.all()
    form = ProductForm()
    
    return render_template("inventory.html", inventory=recent_orders, products=products,form = form )

@bp.route("/inventory/add", methods=['POST'])
@login_required

def add_inventory():
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity')
    if product_id and quantity:
        new_inventory = InventoryModel(
            product_id=int(product_id),
            quantity=int(quantity)
        )
        db.session.add(new_inventory)
        db.session.commit()
        flash("库存添加成功", 'success')
    return redirect(url_for('qa.inventory'))

@bp.route("/inventory/delete/<int:inventory_id>")
@login_required

def delete_inventory(inventory_id):
    record = InventoryModel.query.get_or_404(inventory_id)
    db.session.delete(record)
    db.session.commit()
    flash("库存记录删除成功", 'success')
    return redirect(url_for('qa.inventory'))

@bp.route("/orders")
@login_required
def orders():
    orders = OrdersModel.query.all()
    customers = CustomersModel.query.all()
    products = ProductsModel.query.all()
    form = OrderForm()
    return render_template("orders.html", orders=orders, customers=customers, products=products, form=form)

@bp.route("/orders/add", methods=['POST'])
@login_required
def add_order():
    form = OrderForm(request.form)
    form.customer_id.choices = [(c.id, c.usename) for c in CustomersModel.query.all()]
    form.product_id.choices = [(p.id, p.usename) for p in ProductsModel.query.all()]
    
    if form.validate_on_submit():
        new_order = OrdersModel(
            type=form.type.data,
            money=form.money.data,
            status=form.status.data,
            customer_id=form.customer_id.data,
            product_id=form.product_id.data
        )
        db.session.add(new_order)
        db.session.commit()
        flash("订单添加成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.orders'))
@bp.route("/orders/edit/<int:order_id>", methods=['POST'])
@login_required
def edit_order(order_id):
    order = OrdersModel.query.get_or_404(order_id)
    form = OrderForm(request.form, obj=order)
    form.customer_id.choices = [(c.id, c.usename) for c in CustomersModel.query.all()]
    form.product_id.choices = [(p.id, p.usename) for p in ProductsModel.query.all()]
    
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash("订单信息更新成功", 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'error')
    return redirect(url_for('qa.orders'))

@bp.route("/orders/delete/<int:order_id>")
@login_required
def delete_order(order_id):
    order = OrdersModel.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash("订单删除成功", 'success')
    return redirect(url_for('qa.orders'))