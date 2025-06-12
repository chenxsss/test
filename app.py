from flask import Flask,session,g,render_template,redirect,url_for,flash
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import config
from  exts import db,mail,scheduler
from decorators import login_required
from blueprints.qa import bp as qabp
from blueprints.auth import bp as authbp
from models import UserModel,ProductsModel,InventoryModel,OrdersModel
from sqlalchemy import func
from datetime import datetime, timedelta
app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app,db)
app.register_blueprint(qabp)
app.register_blueprint(authbp)
csrf = CSRFProtect()
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id :
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)#必须设置，不然使用时报错
        #g.user 全局变量
@app.context_processor
def my_context_processor():
    return {"user":g.user}


# app.py
@app.route("/")
@login_required
def index():
    # 获取当前用户的ID（假设每个用户有独立库存）
    user_id = session.get('user_id')
    
    # 确保获取到有效的用户ID
    if not user_id:
        flash("用户未登录", "error")
        return redirect(url_for("auth.login"))
    
    # 修正后的库存查询
    # 需要关联产品表获取库存数量
    total_inventory = db.session.query(func.sum(InventoryModel.quantity)).scalar() or 0
    # 待处理订单查询
    pending_orders = OrdersModel.query.filter_by(status="待处理").count()
    # 低库存预警查询
    low_stock_count = InventoryModel.query.filter(InventoryModel.quantity < 10).count()
    
    # 最近30天销售额计算
    thirty_days_ago = datetime.now() - timedelta(days=30)
    monthly_sales = db.session.query(
        func.sum(OrdersModel.money)
    ).filter(
        OrdersModel.create_time >= thirty_days_ago
    ).scalar() or 0
    
    # 获取最近5条订单
    recent_orders = OrdersModel.query.order_by(OrdersModel.create_time.desc()).limit(5).all()
    
    return render_template('index.html', 
                          total_inventory=total_inventory, 
                          pending_orders=pending_orders, 
                          low_stock_count=low_stock_count, 
                          monthly_sales=monthly_sales, 
                          recent_orders=recent_orders)

@app.template_filter('format_date')
def format_date(value):
    """在模板中格式化日期的安全方式"""
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    elif isinstance(value, str):
        # 尝试解析字符串日期
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return dt.strftime('%Y-%m-%d')
        except:
            return value[:10]  # 简单截取日期部分
    else:
        return str(value) 



if __name__ == "__main__":
    app.run()
