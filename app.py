from flask import Flask, render_template, request, session, redirect, url_for,flash,get_flashed_messages,jsonify
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import and_ 
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
from datetime import timedelta
from bs4 import BeautifulSoup
# import json
##
###############------------##################

app = Flask(__name__)
app.secret_key = "eldosh"  # Replace with your own secret key
# app.permanent_session_lifetime = timedelta(minutes=30)

login_manager=LoginManager(app) #idetifies the app that loginManager start to set policies for it
login_manager.login_view='login' #specify the name of the view function (or the endpoint) that handles user logins. When an unauthorized user attempts..
                                 # ,to access a route or a resource that requires the user to be logged in.. 
                                 # ,Flask-Login automatically redirects the user to the URL associated with the view function specified in login_manager.login_view.

#use current_user to get the currently logged in user\

@login_manager.user_loader
def load_user(user_id):
    tourist_id=user_id
    tourguide_id=user_id
    tourist = Tourist.query.get(int(tourist_id))
    if tourist:
        return tourist
    tourguide = TourGuide.query.get(int(tourguide_id))
    # tourguide = TourGuide.query.filter_by(tourguide_id=tourguide_id).first()
    return tourguide if tourguide else None
###
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

#
##---------------------------------------------##
#ORM : Tables
class TourGuide(db.Model):
    __tablename__ = 'tourguide'

    tourguide_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    first_lang = db.Column(db.String(50), nullable=True)
    second_lang = db.Column(db.String(50), nullable=True)
    third_lang = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    verified = db.Column(db.Integer, nullable=True)
    verification_token = db.Column(db.String(64), nullable=False)
    accepted_requests=db.Column(db.Integer, nullable=True)
    rejected_requests=db.Column(db.Integer, nullable=True)
    ignored_requests=db.Column(db.Integer, nullable=True)
        

    @property
    def is_active(self):
        return True  

    def get_id(self): #Always ensure that get_id() returns a unique identifier for each user, 
                      #and that it's consistent with how your application retrieves users in the user loader callback.
        return str(self.tourguide_id)
        
    def __repr__(self):
        return f"<TourGuide {self.first_name} {self.second_name}>"

class Hotels(db.Model):
    __tablename__ = 'Hotels'
    Hotel_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(100), nullable=True)  
    Opening = db.Column(db.Date, nullable=True)  
    Owner = db.Column(db.String(100), nullable=True)  
    Rooms = db.Column(db.String(100), nullable=True) 
    city_id = db.Column(db.Integer, nullable = True) 

    def get_id(self):
        return str(self.Hotel_ID)

class Cities_data(db.Model):
    __tablename__ = 'cities_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    latitude = db.Column(db.Float, nullable = False)

    def get_id(self):
        return str(self.id)

class Tourist(db.Model, UserMixin):  # Inherit from UserMixin
    __tablename__ = 'tourist'

    tourist_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)  # Unique phone number
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email
    password = db.Column(db.String(100), nullable=False)  # Hashed password
    nationality = db.Column(db.String(50), nullable=False)
    passport = db.Column(db.String(50), nullable=False) 
    verified = db.Column(db.Boolean, default=False)  # Verified flag
    verification_token = db.Column(db.Integer, default=0)  # Token for email verification

    # Adding the required property 'is_active' for Flask-Login
    @property
    def is_active(self):
        return True  # You can customize this logic (e.g., check 'verified')

    def get_id(self): #Always ensure that get_id() returns a unique identifier for each user, 
                      #and that it's consistent with how your application retrieves users in the user loader callback.
        return str(self.tourist_id)

    def __repr__(self):
        return f"<Tourist {self.first_name} {self.second_name}>"

class TouristRequest(db.Model):
    __tablename__ = 'touristrequest'
    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    meeting_point = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    tourist_id_fk_req = db.Column(db.Integer,db.ForeignKey('tourist.tourist_id'), nullable=True)

    #Relationships:
    tourist_fk_req = db.relationship('Tourist', backref='TouristRequest')

class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tourguide_id_fk = db.Column(db.BigInteger, db.ForeignKey('tourguide.tourguide_id'), nullable=False)
    tourist_id_fk = db.Column(db.BigInteger, db.ForeignKey('tourist.tourist_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('touristrequest.id'), nullable=False)

    # Relationships
    tour_guide = db.relationship('TourGuide', backref='schedule')
    tourist = db.relationship('Tourist', backref='schedule')

    reservation = db.relationship('TouristRequest', backref='schedule')

    # def __repr__(self):
    #     return f"<Schedule(id={self.id}, tour_guide_id={self.tour_guide_id}, date={self.date}, reservation_id={self.reservation_id})>"

class Historical(db.Model):
    __tablename__='Historical'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    location=db.Column(db.String(1000),nullable=False)
    name=db.Column(db.String(200),nullable=False)
    type_=db.Column(db.String(100),nullable=False)

class Rejected_Tours(db.Model):
    __tablename__ = 'rejected_tours'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tourguide_id_fk_rej = db.Column(db.BigInteger, db.ForeignKey('tourguide.tourguide_id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('touristrequest.id'), nullable=False)
    
    # Relationships
    fk_tourguide_rej = db.relationship('TourGuide', backref='Rejected_Tours')
    fk_touristrequest_rej = db.relationship('TouristRequest', backref='Rejected_Tours')

# class User(UserMixin,db.Model):
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #Defining Attributes
#     first_name=db.Column(db.String(50))
#     second_name=db.Column(db.String(50))
#     email_address=db.Column(db.String(50), unique=True)
#     password=db.Column(db.String(50))
#     phone=db.column(db.String(50))
#     verified = db.Column(db.Integer, default=0)  # Email verification status
#     verification_token = db.Column(db.String(64), default=lambda: secrets.token_hex(32))

#     def get_id(self): #Always ensure that get_id() returns a unique identifier for each user, 
#                       #and that it's consistent with how your application retrieves users in the user loader callback.
#         return str(self.user_id)

# with app.app_context():
#     db.create_all()

##----------------------------------------------##
# name , location, open, owner, rooms, 

tokens = {}

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
    return rand_code_global

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

####################################################################################################
@app.route("/")
def home(): #main-page

    return render_template("home.html",pagetitle="TimelessTraveller") # Loading the HTML page

@app.route("/choose_feature")
def choose_feature(): #main-page

    return render_template("feature.html",pagetitle="TimelessTraveller") # Loading the GET Started Button


@app.route("/select")
def select(): 
    return render_template("Selection_page.html",pagetitle="TimelessTraveller") 

@app.route("/Request_Tourguide", methods=['GET', 'POST'])
def Request_Tourguide():
    if request.method == 'POST':
        tourist_id=session.get('tourist_id')
        current_tourist=Tourist.query.get(tourist_id)
        tour_name = request.form['tour_name']
        date = request.form['date']
        location = request.form['location']
        meeting_point = request.form['meeting_Point']
        new_request = TouristRequest(
            tour_name=tour_name, 
            date=datetime.strptime(date, '%Y-%m-%d'),
            location=location, 
            meeting_point=meeting_point,
            tourist_id_fk_req = tourist_id
        )
        db.session.add(new_request)
        db.session.commit() 
        return redirect(url_for('Tourist_selection_page'))
    return render_template("Request_Tourguide.html",pagetitle="TimelessTraveller") 

@app.route("/Tourist_selection_page")
def Tourist_selection_page(): 
    tourist_id=session.get('tourist_id')
    current_tourist=Tourist.query.get(tourist_id)
        #Pending Requests
    # pending_reuests = TouristRequest.query.filter_by(
    #     and_(
    #         TouristRequest.status == 'Pending',
    #         TouristRequest.id ==tourist_id     
    #         )
    # ).all()
    #Tourist Accepted Requests
    # accepted_tours = db.session.query(Schedule, TouristRequest).join(
    # TouristRequest, Schedule.reservation_id == TouristRequest.id
    # ).filter(Schedule.tourist_id_fk == tourist_id).all()

    # flash("Tour Request Submitted Successfully!")
    # return redirect(url_for('Tourist_selection_page'))

    return render_template("Tourist_selection_page.html", tourist_id=tourist_id, pagetitle="TimelessTraveller") 


## Tourguide:
@app.route("/Tour_guide_dashboard",methods=['POST','GET']) ##
def tourguide_dashboard(): 
    current_tourguide_id = session.get('tourguide_id')
    current_tourguide=TourGuide.query.get(current_tourguide_id)
    # current_tourguide_id = 1
    print(current_tourguide_id, " hi")
    # current_tourguide_id = session['tourguide_id']

    #Requests in Schdeules (Confirmed or Finished)
    # Query for "Upcoming" requests: status = 'confirmed'
    
    request_upcom = TouristRequest.query.join(Schedule, Schedule.reservation_id == TouristRequest.id)\
        .filter(and_(Schedule.tourguide_id_fk == current_tourguide_id, TouristRequest.status == 'confirmed'))\
        .all()

    # Query for "Previous" requests: status = 'finished'
    request_prev = TouristRequest.query.join(Schedule, Schedule.reservation_id == TouristRequest.id)\
        .filter(and_(Schedule.tourguide_id_fk == current_tourguide_id, TouristRequest.status == 'finished'))\
        .all()

    #When Tourguide click Accept or Reject:
    if request.method == 'POST':
        
        form_type = request.form.get('form_type')
        if form_type == 'form1':
            email_edit=request.form['email']
            password=request.form['password']
            # Renwing The Email:
            current_tourguide.email=email_edit
            current_tourguide.password=password
            db.session.commit()
        
        else:
            request_id = 1
            tourguide_id = 1
            action = 1  # 'accept' or 'reject' 

            request_id = request.form['request_id']
            tourguide_id = current_tourguide_id
            action = request.form['action']  # 'accept' or 'reject' 
            

            if action == 'accept':
                # Mark the request as confirmed and add it to Schdelule
                request_entry = TouristRequest.query.get(request_id)
                request_entry.status = 'confirmed'
                accepted_tour = Schedule(
                    tourist_id_fk=request_entry.tourist_id_fk_req,
                    tourguide_id_fk=tourguide_id,
                    date=request_entry.date,
                    reservation_id=request_id
                  #guide_id = current_tourguide_id
                )
                db.session.add(accepted_tour)
                db.session.commit()

            elif action == 'reject':
                # Mark the request as rejected (or remove it from the guide's view)
                request_id = request.form.get('request_id')
                request_entry = TouristRequest.query.get(request_id)
                request_entry.status = 'rejected'
                new_reject= Rejected_Tours(
                    tourguide_id_fk_rej=current_tourguide_id,
                    request_id=request_id
                )
                db.session.add(new_reject)
                db.session.commit()




    # Query for "Pending" requests for all tour guides (if user rejects it removed from his page of requests)
##

    requests_rejected = TouristRequest.query.join(Rejected_Tours, Rejected_Tours.request_id == TouristRequest.id)\
        .filter(TouristRequest.status == 'Pending')\
        .all()
    
    rejected_request_ids = [request.id for request in requests_rejected if request.tourguide_id_fk]

    requests_pending=TouristRequest.query.filter_by(status='Pending').all()
    
    final_pending_requests = [request for request in requests_pending if request.id not in rejected_request_ids]


    # requests = TouristRequest.query.filter_by(status='Pending').all()
    # return render_template('guides.html', requests=requests) ##byb3t dictionary b kol al requests w t4t8l b for loop fy jinja
    return render_template("Tour_guide_dashboard.html",
                            current_tourguide=current_tourguide,
                            requests=requests_pending,
                            request_upcom=request_upcom,
                            request_prev=request_prev,
                            final_pending_requests=final_pending_requests,
                            pagetitle="TimelessTraveller") 



# def tourguide_dashboard(): 
#     requests = TouristRequest.query.filter_by(status='Pending').all()
#     # return render_template('guides.html', requests=requests) ##byb3t dictionary b kol al requests w t4t8l b for loop fy jinja
#     return render_template("Tour_guide_dashboard.html", requests=requests,pagetitle="TimelessTraveller") 

#
# Send a GET request to the page


def extract_info_hotel(h_name):
    data = h_name
    url = f"https://en.wikipedia.org/wiki/{data}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    name = soup.find("h1", {"id": "firstHeading"}).text.strip()

    infobox = soup.find("table", {"class": "infobox"})
    rows = infobox.find_all("tr") if infobox else []

    location, opening, owner, rooms = None, None, None, None

    for row in rows:
        header = row.find("th")
        data = row.find("td")

        if header and data:
            header_text = header.text.strip().lower()

            if "location" in header_text:
                location = data.text.strip()
            elif "opening" in header_text:
                opening = data.text.strip()
            elif "owner" in header_text:
                owner = data.text.strip()
            elif "number of rooms" in header_text:
                rooms = data.text.strip()

    return {
        "Name": name,
        "Location": location,
        "Opening": opening,
        "Owner": owner,
        "Number of Rooms": rooms,
    }

wikipedia_links = [
    "Cecil_Hotel_(Alexandria)",
    "El_Safa_Palace",
    "Cairo_Marriott_Hotel",
    "Fairmont_Nile_City",
    "Grand_Nile_Tower_Hotel",
    "Mena_House_Hotel",
    "Semiramis_InterContinental_Hotel",
    "Sofitel_Cairo_Nile_El_Gezirah_Hotel",
    "Windsor_Hotel_(Cairo)",
    "Steigenberger_Hotel_%26_Nelson_Village",
    "Old_Cataract_Hotel"
]

def update_hotels():
    for hotel_link in wikipedia_links:
        info = extract_info_hotel(hotel_link)
        current_hotel = Hotels(
            Name = info['Name'],
            Location = info['Location'],
            Opening = info['Opening'],
            Owner = info['Owner'],
            Rooms = info['Number of Rooms']
        )
        db.session.add(current_hotel)
        db.session.commit()

@app.route("/Historical_Sites",methods=['POST','GET'])
def Historical_sites(): 
    update_hotels()
    if request.method == 'POST':
        hotel_name = request.form.get('hotel_name')
        print(hotel_name)
        hotel = Hotels.query.filter_by(Name=hotel_name).first()
        if hotel:
            return render_template("Historical_Sites.html", Hotel_name = hotel_name,
                                    location = hotel.Location,
                                    opening = hotel.Opening,
                                    Owner = hotel.Owner,
                                    rooms = hotel.Rooms)
        else:
            flash(f"Hotel Not Found")
            return redirect(url_for('Historical_Sites'))
    return render_template("Historical_Sites.html") 

@app.route('/verify/<token>')
def verify_account(token):
    global tokens
    token_data = tokens.get(token)
    if token_data:
        if time.time() - token_data["timestamp"] < 3600:
            user = Tourist.query.filter_by(email= tokens[token]["email"]).first() ##EDITTT DONE CHECK
            if not user:
                user = TourGuide.query.filter_by(email = tokens[token]["email"]).first() ##EDITTT DONE CHECK

            user.verified = True
            user.verification_token = token
            db.session.commit()
            return render_template("Email_verfication.html", pagetitle="Email_verification", verification_message = "Your account has been successfully verified", redirect_message = url_for("home"))
        else:
            del tokens[token]  # Token expired, remove it
            return render_template("Email_verfication.html", pagetitle="Email_verification", verification_message = "Token Expired!", redirect_message = url_for("login"))
    else:
        return render_template("Email_verfication.html", pagetitle="Email_verification", verification_message = "Invalid or expired Token!", redirect_message = url_for("login"))

def strong_pass(password):
    return len(password) >=8 and len(password) <=20 and any(char.isupper() for char in password) and not password.isalnum() and any(char.islower() for char in password) and any(char.isdigit() for char in password)

@app.route("/register_tourist", methods=['POST', 'GET'])
def register_tourist():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        phone = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        nationality= request.form.get('Nationality')
        passport= request.form.get('Passport')
        if not strong_pass(password):
            flash(f"Weak Password")
            return redirect(url_for('register_tourist'))
        else:
        # Email validation
            try:
                valid = validate_email(email)
                email = valid.email  
            except EmailNotValidError as e:
                flash(f"Invalid email: {str(e)}", "error")
                return redirect(url_for('register_tourist'))
            user_exist = Tourist.query.filter_by(email=email).first()
            if user_exist is None:
                hashed_password = password #generate_password_hash(password, method='sha256')
                new_user = Tourist(
                    first_name=first_name,
                    second_name=second_name,
                    phone=phone,
                    email=email,
                    password=hashed_password,
                    nationality=nationality,
                    passport=passport,
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
    return render_template('Registration_Tourist.html', pagetitle="Registration")



@app.route("/register_tourguide", methods=['POST', 'GET'])
def register_tourguide():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        phone = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')
        company_name= request.form.get('Company_name')
        first_lang= request.form.get('first_lang')
        second_lang=request.form.get('second_lang')
        third_lang=request.form.get('third_lang')
        city=request.form.get('City')
        if not strong_pass(password):
            flash(f"Weak Password")
            return redirect(url_for('register_tourguide'))
        else:
        # Email validation
            try:
                valid = validate_email(email)
                email = valid.email  
            except EmailNotValidError as e:
                flash(f"Invalid email: {str(e)}", "error")
                return redirect(url_for('register_tourguide'))
            user_exist = TourGuide.query.filter_by(email=email).first()
            if user_exist is None:
                hashed_password =password #generate_password_hash(password, method='sha256')
                new_user = TourGuide(
                    first_name=first_name,
                    second_name=second_name,
                    phone=phone,
                    email=email,
                    password=hashed_password,
                    company_name=company_name,
                    first_lang=first_lang,
                    second_lang=second_lang,
                    third_lang=third_lang,
                    city=city, 
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

    return render_template('Registration_TourGuide.html', pagetitle="Registration")





# @app.route("/login",methods=['POST','GET'])
# def login():
#     if request.method=="POST":
#         email_ret=request.form.get('email_address')
#         pass_ret=request.form.get('password')
#         email_found=User.query.filter_by(email_address=email_ret).first()
#         # next_page=request.args.get('next')
        
#         if email_found and email_found.password==pass_ret:
#             if email_found.verified==0:
#                 send_email(123,True,email_ret)
#                 flash('unverified email a verification email will be sent')

#             else:
#                 # if next_page:
#                 #   return redirect(url_for(next_page))
#                 login_user(email_found)
#                 return redirect(url_for('registration'))
                

#         else:
#             flash('Invalid email or password')
        
#     return render_template("login.html", pagetitle="login") # Loading the HTML page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email_address')
        password = request.form.get('password')
        
        tourist = Tourist.query.filter_by(email=email).first()
        if tourist and tourist.password == password:
            if tourist.verified==0:
                send_email(123,True,email)
                flash('unverified email a verification email will be sent')

            else:
                # if next_page:
                #   return redirect(url_for(next_page))
                session['tourist_id']=tourist.tourist_id
                login_user(tourist)
                return redirect(url_for('Tourist_selection_page'))

        tourguide = TourGuide.query.filter_by(email=email).first()
        if tourguide and tourguide.password == password:
            if tourguide.verified==0:
                send_email(123,True,email)
                flash('unverified email a verification email will be sent')

            else:
                # if next_page:
                #   return redirect(url_for(next_page))
                session['tourguide_id']=tourguide.tourguide_id
                login_user(tourguide)
                return redirect(url_for('tourguide_dashboard'))
        
        if not tourguide and not tourist:

            flash("Invalid credentials")

    return render_template('login.html')


reset_pass_email=""
@app.route("/Find_Email.html",methods=['POST','GET'])
def forget_pass():
        global reset_pass_email
        global rand_code_global
        if request.method=="POST":
            email_req=request.form.get('email_address')
            email_found=Tourist.query.filter_by(email=email_req).first()##EDITTT DONE CHECK
            if not email_found:
                email_found=TourGuide.query.filter_by(email=email_req).first()##EDITTT DONE CHECK
            rand_code_global=generate_code()

            if email_found:
                reset_pass_email=email_req
                send_email(rand_code_global,False,reset_pass_email)
                return render_template("Verify_Code.html",pagetitle="Forget Password")

            else:
                flash('Invalid email')

        return render_template("Find_Email.html",pagetitle="Forget Password")

attempts=0
@app.route("/verify_code",methods=['POST','GET'])
def verify_code():
    global flag
    global rand_code_global
    global attempts

    if request.method=="POST":
        
        code_req=request.form.get('code')

        if rand_code_global==int(code_req):
            attempts=0
            return render_template("Change_Password.html",pagetitle="Forget Password")
        else:
            if attempts>=2:
                attempts=0
                flash('Invalid code')

            else:    
                flash('try again')
                rand_code_global=generate_code()
                send_email(rand_code_global,False, reset_pass_email)
                attepmts+=1
                return render_template("Verify_Code.html",pagetitle="Forget Password")

    return render_template("login.html")



@app.route("/update_pass",methods=['POST','GET'])
def update_pass():
    verf_pass=""
    new_pass=""
    global reset_pass_email

    if request.method=="POST":
        new_pass=request.form.get('new_pass')
        verf_pass=request.form.get('verf_pass')
        email_found=Tourist.query.filter_by(email=reset_pass_email).first()
        if  not email_found:  
            email_found=TourGuide.query.filter_by(email=reset_pass_email).first()

    if new_pass == verf_pass:
        email_found.password=new_pass
        db.session.commit()
        return render_template("login.html",pagetitle="Login")

    else:
        flash('Unmatched password')

    return render_template("Change_Password.html",pagetitle="Login")



# @app.route("/tour_guide_profile",methods=['POST','GET'])
# def tour_guide_profile():
#     current_tourguide_id = session.get('tourguide_id')

#     Tourist_guide=Tourguide.query.filter_by(tourguide_id=current_tourguide_id).first()
#     flash(Tourist_guide.first_name)
#     return render_template("Tour_guide_dashboard.html")




@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    # db.create_all()  # Ensure the database is set up
    app.run(debug=True, port=5000)


####