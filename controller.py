from flask import *   
from flask_mail import *
from datetime import date
from datetime import datetime
import uuid
# from model.model import Hackaholics

app=Flask(__name__)
app.secret_key = "div"

mail = Mail(app)

import datetime
app = Flask(__name__) #creating the Flask class object  
app.secret_key="div"

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = '19euit046@skcet.ac.in'  
app.config['MAIL_PASSWORD'] = 'gauniganesh'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        return render_template("Landing_Home.html")

@app.route('/Login',methods=["POST","GET"])
def Login():
    if request.method=="GET":
        return render_template("Login.html")

@app.route('/Register',methods=["POST","GET"])
def Register():
    if request.method=="GET":
        return render_template("Login.html")

@app.route('/DonorSearch',methods=["POST","GET"])
def Donor_Search():
    if request.method=="GET":
        return render_template("Donor_Search.html")

@app.route('/DonorFilter',methods=["POST","GET"])
def Donor_Filter():
    if request.method=="POST" or request.method=="GET":
        return render_template("Donor_Filter.html")

@app.route('/Donate',methods=["POST","GET"])
def Donate():
    if request.method=="GET":
        return render_template("Recipient_Filter.html")

if(__name__=="__main__"):
    app.run(debug=True)
