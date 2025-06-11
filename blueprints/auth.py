from flask import Blueprint,jsonify,url_for,session,g,flash
from flask import render_template,redirect,request
from exts import mail,db
from flask_mail import Message
from models import UserModel,EmailCaptchaModel
from forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
from email_validator import validate_email, EmailNotValidError
import random,string
bp = Blueprint("auth",__name__,url_prefix="/auth")


@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            emai_user=form.email.data
            password = form.password.data
            if '@' in emai_user:
                user = UserModel.query.filter_by(email = emai_user).first()      
            else:
                user = UserModel.query.filter_by(username = emai_user).first()
            if not user:
                print("非法用户或者邮箱登录")
                flash("用户不存在",'error')
                return redirect(url_for('auth.login'))#后期改成消息闪现的形式
            if check_password_hash(user.password,password):
                #cookie
                # 不适合存放太多的数据，只适合存少量
                # 一般用来存储登录授权的东西
                # flask中的session是经过加密存储在cookie中的,需要
                session['user_id']=user.id
                return redirect(url_for("index"))

            else :
                print("密码错误")
                flash('密码错误','error')
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            flash(f'{form.errors}','error')
            return redirect(url_for("auth.login"))





@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method== 'GET':
        return render_template("register.html") 
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data        
            user = UserModel(email = email,username = username,password = generate_password_hash(password))
                                                                     #密码不能明文存储，所以这里用自带加密
            db.session.add(user)
            db.session.commit()
            flash("注册成功",'success')
            return  redirect(url_for("auth.login"))
        else:
            print(form.errors)
            flash(f"{form.errors}",'error')
            return redirect(url_for("auth.register"))
    
@bp.route("/captcha/email")
def get_email_captcha():
   # email = request.args.get("mail")
    email = request.args.get("email","").strip()
    if not email:
        return jsonify(code=400, message="邮箱参数不能为空")
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        return jsonify({"code": 400, "message": "邮箱格式无效"})
    # source =string.digits*4
    # captcha = random.sample(source,4)
    # delemail =EmailCaptchaModel.query.filter_by(email=email)
    # if delemail:
    #     db.session.delete(delemail)
    #     db.session.commit()
    # captcha = "".join(captcha)
    # message = Message(subject="秘贴验证码",recipients=[email],body=f"您的验证码是{captcha}")
    # mail.send(message)
    old_records = EmailCaptchaModel.query.filter_by(email=email).all()
    if old_records:
        for record in old_records:
            db.session.delete(record)
    
    # 生成4位数字验证码
    captcha = ''.join(random.choices(string.digits, k=4))
    
    # 保存到数据库
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
    return jsonify({"code":200,"message":"邮件发送成功"})