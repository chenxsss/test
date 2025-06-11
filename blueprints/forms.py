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