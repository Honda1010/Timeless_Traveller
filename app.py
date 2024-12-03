from flask import Flask, render_template, request, session, redirect, url_for,flash,get_flashed_messages,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_login import  UserMixin  
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import  login_user, logout_user,login_manager, LoginManager 
from flask_login import login_required, current_user
from flask_mail import Mail, Message
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

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:<desha_uwk003>@<tl-traveller.c9ogmiy8e7zm.eu-north-1.rds.amazonaws.com>/<tl-traveller>'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/hnn' # username: root, password: blank, database_name: hms
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

with app.app_context():
    db.create_all()

##----------------------------------------------##

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'youssifmo0310@gmail.com@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
mail = Mail(app)

@app.route("/")
def homepage(): #main-page
    return render_template("home.html", pagetitle="Homepage") # Loading the HTML page


@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        email_ret=request.form.get('email_address')
        pass_ret=request.form.get('password')
        email_found=User.query.filter_by(email_address=email_ret).first()

        if email_found and email_found.password==pass_ret:
            login_user(email_found)
            return redirect(url_for('/'))

        else:
            flash('Invalid email or password')
    
    return render_template("login.html", pagetitle="login") # Loading the HTML page


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email').lower()  # Normalize email
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
            hashed_password = password #generate_password_hash(password, method='sha256')
            new_user = User(
                first_name=first_name,
                second_name=second_name,
                phone=phone_number,
                email_address=email,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            send_verification_email(new_user)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Email already exists. Please log in.", "error")
            return redirect(url_for('login'))

    return render_template("registration.html", pagetitle="Registration")
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()  # Ensure the database is set up
    app.run(debug=True, port=5000)  