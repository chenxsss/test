#配置文件
#数据库配置
HOSTNAME = "127.0.0.1"
PORT     = '3306'
DATABASE = 'jxc'
USERNAME = 'root'
PASSWORD = '123456'
DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URL


#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL =True
MAIL_PORT= 465
MAIL_USERNAME = "2774154583@qq.com"
MAIL_PASSWORD = "qfaewgatjwltdcce"
MAIL_DEFAULT_SENDER = "2774154583@qq.com"

#密令
SECRET_KEY= "lpko1234djfsks885d"