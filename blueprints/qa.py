from flask import Blueprint,jsonify,url_for,session,g,flash
from flask import render_template,redirect,request
from exts import mail,db
from flask_mail import Message
bp = Blueprint("qa",__name__,url_prefix="/qa")