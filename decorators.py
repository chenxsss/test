from functools import wraps
from flask import g ,redirect,url_for

def login_required(func):#wraps 装饰器保留原来函数的信息
    #保留func信息
    @wraps(func)
    #func(a,b,c)
    #inner实现保留func的信息，func还可能有参数*args,**kwargs万能参数
    def inner(*args,**kwargs):
        if g.user:
            return func(*args,**kwargs)#如果有就传参数         #hasattr(g,"user"):#判断g上面有没有“user”，但是也有可能是None
                                                     
        else:
            return redirect(url_for("auth.login"))

    return inner