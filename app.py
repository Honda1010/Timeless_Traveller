from flask import Flask, render_template, request, session, redirect, url_for,flash,get_flashed_messages,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_login import  UserMixin  
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import  login_user, logout_user,login_manager, LoginManager 
from flask_login import login_required, current_user
from flask_mail import Mail, Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import time
from werkzeug.security import generate_password_hash
from email_validator import validate_email, EmailNotValidError
import secrets
import random
import requests
from bs4 import BeautifulSoup
import time
import atexit
from datetime import datetime
import smtplib
from email.message import EmailMessage
# import secrets
import string
from flask_migrate import Migrate
# import json
##
###############------------##################

app = Flask(__name__)
app.secret_key = "eldosh"  # Replace with your own secret key


login_manager=LoginManager(app) #idetifies the app that loginManager start to set policies for it
login_manager.login_view='login' #specify the name of the view function (or the endpoint) that handles user logins. When an unauthorized user attempts..
                                 # ,to access a route or a resource that requires the user to be logged in.. 
                                 # ,Flask-Login automatically redirects the user to the URL associated with the view function specified in login_manager.login_view.

@login_manager.user_loader
def load_user(user_id):
    user=user.query.get(str(user_id))
    return user
##
##
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:<desha_uwk003>@<tl-traveller.c9ogmiy8e7zm.eu-north-1.rds.amazonaws.com>/<tl-traveller>'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/tl_traveller' # username: root, password: blank, database_name: hms
db=SQLAlchemy(app) #creating object(Database) of class SQLALCHEMY
migrate = Migrate(app, db)
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

##---------------------------------------------##
#ORM : Tables

class User(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #Defining Attributes
    first_name=db.Column(db.String(50))
    second_name=db.Column(db.String(50))
    email_address=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(50))
    phone=db.column(db.String(50))
    verified = db.Column(db.Boolean, default=False)  # Email verification status
    verification_token = db.Column(db.String(64), default=lambda: secrets.token_hex(32))

    def get_id(self): #Always ensure that get_id() returns a unique identifier for each user, 
                      #and that it's consistent with how your application retrieves users in the user loader callback.
        return str(self.user_id)

# with app.app_context():
#     db.create_all()

##----------------------------------------------##

tokens = {}

def generate_token(user_email): 
    global tokens
    token = hashlib.md5((user_email + str(time.time())).encode()).hexdigest() #unique token for each user hashed
    tokens[token] = {"email": user_email, "timestamp": time.time()} #store tokens in a map
    return token

def send_email(x, verify, recipient_email):
    sender_email = "moustafaalaa30@gmail.com"
    sender_password = "ycdknfumtdszsgzn"   
    if verify == True:
        subject = "Account Verification"
        token = generate_token(recipient_email)
        verification_url = f"http://127.0.0.1:5000/verify/{token}"
        body = f"Please click the following link to verify your account:\n\n{verification_url}"
    else:
        subject = "Password Reset"
        body = f"Please use the following code:\n\n{str(x)}"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  
            server.login(sender_email, sender_password)
            server.send_message(msg)  
            flash('Email sent successfully!')
    except Exception as e:
        flash(f'Failed to send email: {str(e)}')

@app.route('/verify/<token>')
def verify_account(token):
    global tokens
    token_data = tokens.get(token)
    if token_data:
        if time.time() - token_data["timestamp"] < 3600:
            user = User.query.filter_by(email_address = tokens[token]["email"]).first()
            user.verified = True
            user.verification_token = token
            db.session.commit()
            return "Your account has been successfully verified!"
        else:
            del tokens[token]  # Token expired, remove it
            return "Token expired."
    else:
        return "Invalid or expired token."

@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        # Email validation
        try:
            valid = validate_email(email)
            email = valid.email  
        except EmailNotValidError as e:
            flash(f"Invalid email: {str(e)}", "error")
            return redirect(url_for('registration'))
        user_exist = User.query.filter_by(email_address=email).first()
        if user_exist is None:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(
                first_name=first_name,
                second_name=second_name,
                phone=phone_number,
                email_address=email,
                password=hashed_password,
                verified = False,
                verification_token = 0
            )
            db.session.add(new_user)
            db.session.commit()
            send_email(1,True,email)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Email already exists. Please log in.", "error")
    return render_template("registration.html", pagetitle="Registration")

# @app.route("/")
# def home(): #main-page
#     return render_template("login.html", pagetitle="Homepage") # Loading the HTML page

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        email_ret=request.form.get('email_address')
        pass_ret=request.form.get('password')
        email_found=User.query.filter_by(email_address=email_ret).first()

        if email_found.verified==False:
            send_email(123,True,email_found)

        else:
            if email_found and email_found.password==pass_ret:
                login_user(email_found)
                return redirect(url_for('/'))

            else:
                flash('Invalid email or password')
    
    return render_template("login.html", pagetitle="login") # Loading the HTML page

reset_pass_email=""
@app.route("/forget_password",methods=['POST','GET'])
def forget_pass():
        global reset_pass_email
        if request.method=="POST":
            email_req=request.form.get('email_address')
            email_found=User.query.filter_by(email_address=email_req).first()

            if email_found:
                reset_pass_email=email_req
                return redirect(url_for('code'))

            else:
                flash('Invalid email')

        return render_template("forget_password.html",pagetitle="Forget Password")

flag=False
rand_code_global=0

def generate_code():
    global flag
    global rand_code_global
    vref_codes=[]
    rand_code=random.randint(100000,900000)
    while rand_code in vref_codes:
        rand_code=random.randint(100000,900000)
    vref_codes.append(rand_code)
    rand_code_global=rand_code

@app.route("/code",methods=['POST','GET'])
def verify_code():
    global flag
    global rand_code_global

    flag=1
    send_email(rand_code_global,flag,reset_pass_email)
    if 'attempts' not in session:
        session['attempts']=0

    if request.method=="POST":
        
        code_req=request.form.get('code')
        code_found=User.query.filter_by(verification_token=code_req).first()

        if code_found:
            session['attempts']=0
            return redirect(url_for('reset_password'))

        else:
            flash('try again')
            send_email(rand_code_global, flag, reset_pass_email)
            session['attempts']+=1

            if session['attempts']==3:
                flag=0
                flash('Invalid code')

    return render_template("login.html",pagetitle="Login")


@app.route("/reset_password",methods=['POST','GET'])
def update_pass():
    verf_pass=""
    new_pass=""
    if request.method=="POST":
        new_pass=request.form.get('new_pass')
        verf_pass=request.form.get('verf_pass')
    
    if new_pass == verf_pass:
        User.password=new_pass

    else:
        flash('Unmatched password')
        redirect(url_for('reset_password'))    

    return render_template("login.html",pagetitle="Login")
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    # db.create_all()  # Ensure the database is set up
    app.run(debug=True, port=5000)
