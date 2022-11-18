from flask import *   
from flask_mail import *
from datetime import date
from datetime import datetime
import uuid
from model.model import PlasmaModel

app=Flask(__name__)
app.secret_key = "div"

mail = Mail(app)

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
        return render_template("Home.html")

@app.route('/Login',methods=["POST","GET"])
def Login():
    obj = PlasmaModel()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        out=obj.get_user_info_email(email)
        if out:
            if out['PASSWORD']==password:
                return redirect(url_for("Landing_home",id=out['ID'])  )          
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['EMAIL'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("Login.html")

@app.route('/Register',methods=["POST","GET"])
def Register():
    obj = PlasmaModel()
    if request.method=="GET":
        return render_template("sign_up.html")
    elif request.method=="POST":
        Id=uuid.uuid1()
        if int(request.form['age'])<18: 
            flash("Age is under than 18. Cannot register")
            return render_template("sign_up.html")
        if int(request.form['weight'])<50: 
            flash("Weight is under 50. Cannot register")
            return render_template("sign_up.html")

        data={
            'ID':str(Id),
            'NAME':request.form['username'],
            'AGE':request.form['age'],
            'DATE_OF_BIRTH':request.form['dob'],
            'WEIGHT':request.form['weight'],
            'GENDER':request.form['Gender'],
            'AREA':request.form['area'],
            'DISTRICT':request.form['District'],
            'STATE':request.form['State'],
            'EMAIL':request.form['email'],
            'PASSWORD':request.form['password'],
            'MOBILE_NO':request.form['mobileno'],
            'BLOOD_GROUP':request.form['bloodgroup']
        }
        obj.insert_into_users(data)
        flash("Successfully Registered!!")
        return render_template("Login.html")

@app.route('/Landing_home/<id>',methods=["POST","GET"])
def Landing_home(id):
    if request.method=="GET":
        return render_template("Landing_Home.html",id=id)


@app.route('/donorsearch/<id>',methods=["POST","GET"])
def Donor_Search(id):
    if request.method=="GET":
        return render_template("Donor_Search.html",id=id)
    elif request.method=="POST":
        obj = PlasmaModel()
        data={
            'BLOOD_GROUP':request.form['bloodgroup'],
            'STATE':request.form['State'],
            'DISTRICT':request.form['District']
        }
        output=obj.get_user_info_bloodgroup(data)
        return render_template("Donor_Filter.html",data=output,id=id,bloodgroup=request.form['bloodgroup'],state=request.form['State'],district=request.form['District'])

@app.route('/DonorFilter/<id>/<filter>/<bloodgroup>/<state>/<district>',methods=["POST","GET"])
def Donor_Filter(id,filter,bloodgroup,state,district):
    obj = PlasmaModel()
    data={
        'BLOOD_GROUP':bloodgroup,
        'STATE':state,
        'DISTRICT':district
    }
    if request.method=="GET":
        output=obj.get_donor_filter(data,filter)
        return render_template("Donor_Filter.html",data=output,id=id,bloodgroup=bloodgroup,state=state,district=district)

@app.route('/Donate/<id>',methods=["POST","GET"])
def Donate(id):
    if request.method=="GET":
        return render_template("Recipient_Filter.html",id=id)

@app.route('/location_enter/<donor_id>/<donor_name>/<recipient_id>',methods=["POST","GET"])
def Location_enter(donor_id,donor_name,recipient_id):
    obj = PlasmaModel()
    recipient_info=obj.get_user_info_id(recipient_id)
    if request.method=="GET":
        data={
            'DONOR_ID':donor_id,
            'DONOR_NAME':donor_name,
            'RECIPIENT_ID':recipient_id,
            'RECIPIENT_NAME':recipient_info['NAME'],
            'DATE_OF_DONATION':str(date.today()),
            'BLOOD_GROUP':recipient_info['BLOOD_GROUP'],
            'MOBILE_NO':recipient_info['MOBILE_NO'],
            'DISTRICT':recipient_info['DISTRICT'],
            'STATE':recipient_info['STATE'],
            'STATUS':"Pending"
        }
        return render_template("EnterLocation.html",id=recipient_id,data=data)
    if request.method=="POST":
        Id=uuid.uuid1()
        tableData={
            'DONATE_ID':str(Id),
            'DONOR_ID':donor_id,
            'DONOR_NAME':donor_name,
            'RECIPIENT_ID':recipient_id,
            'RECIPIENT_NAME':recipient_info['NAME'],
            'DATE_OF_DONATION':str(date.today()),
            'BLOOD_GROUP':recipient_info['BLOOD_GROUP'],
            'LOCATION':request.form['location'],
            'STATUS':"Pending"
        }
        obj.insert_into_donations(tableData)
        return render_template("Thankyou_request.html",id=recipient_id)



@app.route('/Profile/<id>',methods=["POST","GET"])
def Profile(id):
    obj=PlasmaModel()
    if request.method=="GET":
        output=obj.get_user_info_id(id)
        return render_template("Profile.html",id=id,data=output)
    
    elif request.method=="POST":
        data={
            'NAME':request.form['username'],
            'AGE':request.form['age'],
            'DATE_OF_BIRTH':request.form['dob'],
            'WEIGHT':request.form['weight'],
            'GENDER':request.form['Gender'],
            'AREA':request.form['area'],
            'DISTRICT':request.form['District'],
            'STATE':request.form['State'],
            'EMAIL':request.form['email'],
            'PASSWORD':request.form['password'],
            'MOBILE_NO':request.form['mobileno'],
            'BLOOD_GROUP':request.form['bloodgroup']
        }
        data=obj.update_user_info(data,id)
        return render_template("Profile.html",id=id,data=data)

@app.route('/Logout',methods=["POST","GET"])
def Logout():
    if request.method=="GET":
        return render_template("Home.html")

if(__name__=="__main__"):
    app.run(debug=True)
