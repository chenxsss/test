import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from wtforms.validators import DataRequired
from wtforms import ValidationError
from models import UserModel,EmailCaptchaModel
from datetime import datetime,timedelta
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4,max=4,message="验证码格式错误")])
    username = wtforms.StringField(validators=[Length(min=2,max=20,message="用户名长度3-20个字符")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码长度不够")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致")])

    # 自定义验证：
    # 邮箱是否已经注册
    # 验证码是否正确
    def validate_email(self,field):
        email = field.data
        user  =  UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册")
    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
    
    # 新增三个校验条件
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误！')
        if captcha_model.captcha != captcha:
            raise wtforms.ValidationError(message='验证码错误！')
        if datetime.now() > captcha_model.create_time + timedelta(minutes=5):
            raise wtforms.ValidationError(message='验证码已过期！')
    
        # else: 
        #     db.session.delete(captcha_check)
        #     db.session.commit()
       
       
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[InputRequired(message="不能为空")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])

class RegisterForm(wtforms.Form):
    email = wtforms.StringField('邮箱', validators=[Email(message="邮箱格式错误！"), DataRequired()])
    captcha = wtforms.StringField('验证码', validators=[Length(min=4, max=4, message="验证码格式错误"), DataRequired()])
    username = wtforms.StringField('用户名', validators=[Length(min=2, max=20, message="用户名长度3-20个字符"), DataRequired()])
    password = wtforms.PasswordField('密码', validators=[Length(min=6, max=20, message="密码长度不够"), DataRequired()])
    password_confirm = wtforms.PasswordField('确认密码', validators=[EqualTo("password", message="两次密码不一致")])
    
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError("该邮箱已经被注册")
class SupplierForm(wtforms.Form):
    usename = wtforms.StringField('名称', validators=[DataRequired()])
    linkman = wtforms.StringField('联系人', validators=[DataRequired()])
    pyone = wtforms.StringField('电话', validators=[DataRequired(), Length(min=11, max=11)])
    address = wtforms.StringField('地址', validators=[DataRequired()])
    
class ProductForm(wtforms.Form):
    usename = wtforms.StringField('名称', validators=[DataRequired()])
    standard = wtforms.StringField('规格', validators=[DataRequired()])
    unitprice = wtforms.FloatField('单价', validators=[DataRequired()])
    supplier_id = wtforms.SelectField('供应商', coerce=int, validators=[DataRequired()])

class CustomerForm(wtforms.Form):
    usename = wtforms.StringField('名称', validators=[DataRequired()])
    pyone = wtforms.StringField('电话', validators=[DataRequired(), Length(min=11, max=11)])

class OrderForm(wtforms.Form):
    type = wtforms.StringField('类型', validators=[DataRequired()])
    money = wtforms.StringField('金额', validators=[DataRequired()])
    status = wtforms.StringField('状态', validators=[DataRequired()])
    customer_id = wtforms.SelectField('客户', coerce=int, validators=[DataRequired()])
    product_id = wtforms.SelectField('商品', coerce=int, validators=[DataRequired()])

class OrderForm(wtforms.Form):
    type = wtforms.StringField('类型', validators=[DataRequired()])
    money = wtforms.StringField('金额', validators=[DataRequired()])
    status = wtforms.SelectField('状态', choices=[
        ('待处理', '待处理'),
        ('已发货', '已发货'),
        ('已完成', '已完成')
    ], validators=[DataRequired()])
    customer_id = wtforms.SelectField('客户', coerce=int, validators=[DataRequired()])
    product_id = wtforms.SelectField('商品', coerce=int, validators=[DataRequired()])