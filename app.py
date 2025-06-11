from flask import Flask,session,g,render_template,jsonify
from flask_migrate import Migrate
import config
from  exts import db,mail,scheduler
from decorators import login_required
from blueprints.qa import bp as qabp
from blueprints.auth import bp as authbp
from models import UserModel,ProductsModel,InventoryModel,OrdersModel
from sqlalchemy import func
app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app.db)
app.register_blueprint(qabp)
app.register_blueprint(authbp)

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

@app.route("/")
@login_required()
def index():
    total_inventory = InventoryModel.query.with_entities(func.sum(InventoryModel.quantity)).scalar() or 0
    pending_orders = OrdersModel.query.filter_by(status='待处理').count()
    low_stock_count = ProductsModel.query.join(InventoryModel).filter(InventoryModel.quantity < 10).count()
    monthly_sales = "¥8000.00"  # 实际需计算当月订单总和
    recent_orders = OrdersModel.query.order_by(OrdersModel.create_time.desc()).limit(5).all()
    return render_template('index.html', total_inventory=total_inventory,
                           pending_orders=pending_orders,
                           low_stock_count=low_stock_count,
                           monthly_sales=monthly_sales,
                           recent_orders=recent_orders)



if __name__ == "__main__":
    app.run()
