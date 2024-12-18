from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "eldosh"  # Replace with your own secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:<desha_uwk003>@<tl-traveller.c9ogmiy8e7zm.eu-north-1.rds.amazonaws.com>/<tl-traveller>'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/tl_traveller' # username: root, password: blank, database_name: hms
db=SQLAlchemy(app) #creating object(Database) of class SQLALCHEMY
#
##---------------------------------------------##


class TouristRequest(db.Model):
    __tablename__ = 'touristrequest'
    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    meeting_point = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    guide_id = db.Column(db.Integer, nullable=True)

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

    @property
    def is_active(self):
        return True  

    def get_id(self): #Always ensure that get_id() returns a unique identifier for each user, 
                      #and that it's consistent with how your application retrieves users in the user loader callback.
        return str(self.tourguide_id)
        
    def __repr__(self):
        return f"<TourGuide {self.first_name} {self.second_name}>"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tourist', methods=['GET', 'POST'])
def tourist():
    if request.method == 'POST':
        tour_name = request.form['tour_name']
        date = request.form['date']
        location = request.form['location']
        meeting_point = request.form['meeting_point']
        new_request = TouristRequest(
            tour_name=tour_name, 
            date=datetime.strptime(date, '%Y-%m-%d'), #get the current date and time
            location=location, 
            meeting_point=meeting_point
        )
        db.session.add(new_request)
        db.session.commit()
        # flash("Tour Request Submitted Successfully!")
        return redirect(url_for('home'))
    return render_template('tourist.html')

@app.route('/guides', methods=['GET', 'POST'])
def guides():
    requests = TouristRequest.query.filter_by(status='Pending').all()
    return render_template('guides.html', requests=requests) ##byb3t dictionary b kol al requests w t4t8l b for loop fy jinja

@app.route('/accept/<int:request_id>/<int:guide_id>')#byzhr al request w al guide_id fy al link
def accept(request_id, guide_id):
    tour_request = TouristRequest.query.filter_by(id=request_id, status='Pending').first()
    if tour_request:
        tour_request.status = 'Accepted'
        tour_request.guide_id = guide_id
        db.session.commit()
        flash("You have accepted the request!")
    else:
        flash("Request is no longer available!")
    return redirect(url_for('guides'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
