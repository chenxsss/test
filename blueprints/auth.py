from flask import Blueprint,jsonify,url_for,session,g,flash
from flask import render_template,redirect,request
from exts import mail,db
from forms import LoginForm
from flask_mail import Message
from models import UserModel,EmailCaptchaModel
from forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from email_validator import validate_email, EmailNotValidError
import random,string
bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    # 检查表单提交
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data        
        user = UserModel(
            email=email,
            username=username,
            password=generate_password_hash(password)  # 正确加密密码
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", 'success')
        # ✅ 修复：移除 form 参数
        return redirect(url_for("auth.login"))  
    
    # 显示错误信息
    if form.errors:
        print(form.errors)
        flash(f"{form.errors}", 'error')
    
    # 渲染注册表单（GET请求或验证失败时）
    return render_template("register.html", form=form) 

@bp.route("/login", methods=['GET', 'POST'])
def login():
    # 如果已登录，重定向到首页
    if session.get('user_id'):
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    # 检查表单提交
    if form.validate_on_submit():
        email_or_username = form.email.data
        password = form.password.data
        
        # 根据输入查找用户
        if '@' in email_or_username:
            user = UserModel.query.filter_by(email=email_or_username).first()
        else:
            user = UserModel.query.filter_by(username=email_or_username).first()
        
        if not user:
            flash("用户不存在", 'error')
            # ✅ 返回重新渲染登录页面
            return render_template("login.html", form=form)
        
        # ✅ 验证密码（假设使用了正确的哈希）
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("登录成功", 'success')
            # ✅ 修复：移除 form 参数
            return redirect(url_for("index"))  
        else:
            flash('密码错误', 'error')
            # ✅ 返回重新渲染登录页面
            return render_template("login.html", form=form)
    
    # 渲染登录表单（GET请求或验证失败时）
    return render_template("login.html", form=form)
@bp.route("/logout")
def outlogin():
    session.clear()
    return redirect("/") 

@bp.route("/captcha/email")
def get_email_captcha():
    email = request.args.get("email", "").strip()
    if not email:
        return jsonify(code=400, message="邮箱参数不能为空")
    
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        return jsonify({"code": 400, "message": "邮箱格式无效"})

    # 删除旧验证码
    old_records = EmailCaptchaModel.query.filter_by(email=email).all()
    if old_records:
        for record in old_records:
            db.session.delete(record)
    
    # 生成验证码
    captcha = ''.join(random.choices(string.digits, k=4))
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    
    try:
        message = Message(
            subject="jxcgj",
            recipients=[email],
            body=f"您的验证码是：{captcha}(5分钟内有效)"
        )
        mail.send(message)
    except Exception as e:
        return jsonify({"code": 500, "message": "邮件发送失败"})
    
    return jsonify({"code": 200, "message": "邮件发送成功"})