from flask import Flask, render_template, request, redirect, url_for,flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import date
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from webforms import LoginForm,RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid1
# import imghdr
import os
import shutil
from ultralytics import YOLO
import cv2
import numpy as np
import random

from datetime import datetime, timedelta


app = Flask(__name__)

# Load YOLO model
model = YOLO("yolov8m.pt")
# Define the classes for YOLO model
classes = ["car", "truck", "person"]

def deletePrevRuns():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the "runs" directory
    runs_dir = os.path.join(current_dir, "runs")

    # Define the path to the "temp" directory
    temp_dir = os.path.join(current_dir, "temp")

    # Check if the "runs" directory exists
    if os.path.exists(runs_dir):
        # Delete the "runs" directory and all its contents
        shutil.rmtree(runs_dir)
        print("Directory 'runs' deleted successfully.")
    else:
        print("Directory 'runs' does not exist.")

    # Check if the "temp" directory exists
    if os.path.exists(temp_dir):
        # Delete the "temp" directory and all its contents
        shutil.rmtree(temp_dir)
        print("Directory 'temp' deleted successfully.")
    else:
        print("Directory 'temp' does not exist.")

    return


# Define a function to make predictions on an image
def predict_image(image):
    # Predict Method Takes all the parameters of the Command Line Interface
    output_image=model.predict(source=image, save=True, conf=0.5, save_txt=True)

    return output_image


# Define a function to make predictions on a video
def predict_video(video_path):
    #Predict Method Takes all the parameters of the Command Line Interface
    output_path=model.predict(source=video_path,  save=True, conf=0.5, save_txt=True)
    return output_path
    

# add database
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://freetestdemo:cleopatra2023@db4free.net:3306/freetestdemo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret Key!
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

db = SQLAlchemy(app)
# this cmd run one time !!!!
# db.create_all()
# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	# Do some password stuff!
	password_hash = db.Column(db.String(128))


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Username %r>' % self.username

        
# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form1 = RegistrationForm()
    form2 = LoginForm()

    if request.method == 'POST':
        add_class = request.args.get('add_class') == 'True'
        if form1.submit_reg.data and form1.validate():
            user = Users.query.filter_by(email=form1.email.data).first()
            username = Users.query.filter_by(email=form1.username.data).first()
            if user:
                flash("An account with that email already exists. Please try again.", "alert-warning")
            elif username:
                flash("An account with that username already exists. Please try again.", "alert-warning")
            else:
                hashed_pw = generate_password_hash(form1.password.data, "sha256")
                user = Users(username=form1.username.data, email=form1.email.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
                form1.username.data = ''
                form1.email.data = ''
                form1.password.data = ''
                flash("User Added Successfully! Please log in to continue the process!", "alert-primary")
                return render_template('login.html', form1=form1 , form2=form2 , add_class=True)

        elif form2.submit_log.data and form2.validate():
            user = Users.query.filter_by(username=form2.username.data).first()
            if user and check_password_hash(user.password_hash, form2.password.data):
                login_user(user)
                flash("Login Successful!", "alert-success")
                return render_template('upload.html', add_class=True)

            else:
                flash("Invalid username or password. Please try again.", "alert-danger")

    return render_template('login.html', form1=form1, form2=form2,add_class=True)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!  Thanks For Stopping By...","alert-primary")
	return redirect(url_for('index'))


@app.route('/')
def home():
    return render_template('index.html',add_class = False)


@app.route('/services')
def services():
    return render_template('services.html',add_class = True)


@app.route('/providing')
def providing():
    return render_template('providing.html',add_class = True)

@app.route('/choose')
def choose():
    return render_template('choose.html',add_class = True)

@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        # Save the file
        if not os.path.exists('temp'):
            os.makedirs('temp')
        path = 'temp/' + str(uuid1()) + filename
        file.save(path)
         # Check the file extension for video types
        _, ext = os.path.splitext(filename)
        image_extensions = ['.jpg', '.png', '.bmp']  # Add more video extensions as needed
        if ext.lower() in image_extensions:
            # put model for photo here
            # file_path = 'runs/detect/predict6/e7b73006-1f1d-11ee-bce2-ee5c68d1efa1car.png'
            file_path = ''
            photo_data = predict_image(path)
            # Assuming `result` is a `Results` object with image data
            # photo_data = photo_data.image_data

            # save the output result for photo in photo_data variable
            file_type = 'image'
            #Predict Method Takes all the parameters of the Command Line Interface
            return render_template('result.html',price='350$',file_type=file_type, file_path=file_path,add_class=True)
        else:
           
            video_extensions = ['.mp4', '.avi', '.mov']  # Add more video extensions as needed
            if ext.lower() in video_extensions:
                
                # The file is a video, so make predictions on it
                # input_path = 'temp/' + file.filename
                output_path = predict_video(path)
            else:
                # Handle unsupported file types
                return render_template('result.html',file_type=None,file_path='', price='No price provided',add_class=True)

        # Save the file
        # file.save(save_path)

        return render_template('result.html', file_type=None,file_path='', price='File uploaded successfully.',add_class=True)
    else:
        return render_template('upload.html',add_class=True)


@app.route('/result')
@login_required
def result():
    price = round(random.uniform(10.0, 100.0), 2)
    date = datetime.today() - timedelta(days=random.randint(0, 30))
    add_class = request.args.get('add_class', default=True, type=bool)
    file_type = request.args.get('file_type','')
    file_path = request.args.get('file_path','')
    return render_template('result.html', price=price, date=date, add_class=add_class)

if __name__ == '__main__':
    deletePrevRuns()
    app.run(debug=True)
