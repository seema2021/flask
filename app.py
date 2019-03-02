from flask import Flask,url_for, flash, redirect,jsonify, render_template, request, session, abort
import os,requests,json
import pymysql,hashlib,random
import geocoder
from flask_mail import Mail, Message



app = Flask(__name__)
db = pymysql.connect(
    host="localhost", port=3306, user="root", password="", db="test")
cur = db.cursor()

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
    db = pymysql.connect(host=data['mysql']['host'], port=3306, user=data['mysql']['user'], password=data['mysql']['passwd'], db=data['mysql']['db'])
    cur = db.cursor()
    GOOGLE_GEOCODE_API_KEY=data['api']['GOOGLE_GEOCODE_API_KEY']

    app.config['MAIL_SERVER']=data['mail']['server']
    app.config['MAIL_PORT'] =data['mail']['port'] 
    app.config['MAIL_USERNAME'] = data['mail']['user']
    app.config['MAIL_PASSWORD'] = data['mail']['password']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

#Show login page
@app.route('/',methods=['GET'])
def shaow_login():
    
    return render_template('login.html')

#Show Registration Page
@app.route('/registration',methods=['POST','GET'])
def registration():
    print ("inside registration controller")
    if request.method=='POST':

        name=request.form['Name']
        email=request.form['email']
        number=request.form['Phone-number']
        country=request.form['Country']
        password = encrypt_string(request.form['password'])
        
        #Insert data in registration table
        cur.execute("INSERT INTO registration(name,email,number,city,password) VALUES (%s, %s,%s, %s, %s)", (name, email,number,country,password))
        db.commit()
        return redirect(url_for('do_login'))

    return render_template('registration.html')

#Login Process controller
@app.route('/login', methods=['POST','GET'])
def do_login():
    if request.method=='POST':
        user_name=request.form['email']
        password=encrypt_string(request.form['password'])
        try:
            cur.execute("SELECT COUNT(1) FROM registration WHERE email = %s;", [user_name]) # CHECKS IF USERNAME EXSIST
            if cur.fetchone()[0]:
                cur.execute("SELECT  name,password FROM registration WHERE email = %s;", [user_name]) # FETCH THE HASHED PASSWORD
                for row in cur.fetchall():
                    db_password=row[1];
                    name=row[0]
                
                        
                if(password==db_password):
                    session['logged_in'] = True
                    return redirect(url_for('get_County'))
                else:
                    return render_template('login.html',error='Password does not match')    
            else:
                return  render_template('login.html',error='User not available')       
        except:
            raise
    return render_template('login.html')
#Logout process controller
@app.route('/logout')
def logout():
    session['logged_in']=False
    return render_template("login.html")

#Get hash password
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


#Get country
@app.route('/country',methods=['POST','GET'])
def get_County():
    if not session.get('logged_in'):
         
        return render_template('login.html')
    else:

        if request.method=='POST':
            country=request.form['country']
            session['county']=country
            try:
                
                result = geocoder.google(""+country+",Kenya", key=GOOGLE_GEOCODE_API_KEY)

                if result.country_long=='Kenya':
                    res = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="'+country+'",+Kenya&key=AIzaSyAgg9zZG2mXS6QzgsM3wUbLIljdU6RBmRw')
                    if res.ok:
                        data=res.json()
                        latitude = data['results'][0]['geometry']['location']['lat'] 
                        longitude = data['results'][0]['geometry']['location']['lng'] 
                        formatted_address = data['results'][0]['formatted_address'] 
                        session['longitude']=longitude
                        session['latitude']=latitude
                        # printing the output 
                       # print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
                        #    %(latitude, longitude,formatted_address)) 
                        return jsonify("found")

                else:
                    print ('not in kenya')
                    return jsonify("not found")
                     
            except:    
                print ("inisde except")
                raise
        return render_template('search.html')
        

#Get crop detail based on location
@app.route('/crop',methods=['POST','GET'])
def crop_detail():
    if not session.get('logged_in'):
        
        return render_template('login.html')
    else:

        if request.method=='GET':
            crop=request.args.get('crop')
            
            maturity=request.args.get('maturity')
            tolerance=request.args.get('droughtTolerance')
            county=session['county']
            res = requests.get('http://3.95.145.154/list?x='+str(session['longitude'])+'&y='+str(session['latitude'])+'&crop='+crop+'&maturity='+maturity+'&droughtTolerance='+tolerance+'')
            if res.ok:
                data=res.json()
               
                value=sorted(data, key=lambda x: x['year_of_release_kenya'], reverse=True)
                session['json_data']=value
               
            return render_template("table_result.html",data=value,county=county,crop=crop)
    return render_template('search.html')       

#Send token to mail for update password
@app.route("/forget_password" ,methods=['POST','GET'])
def forget_password_email():
    if request.method=='POST':
        email=request.form['email']
        session['email']=email
        try:
            cur.execute("SELECT COUNT(1) FROM registration WHERE email = %s;", [email]) # CHECKS IF USERNAME EXSIST
            if cur.fetchone()[0]:
          
                token=random.randint(0,100000)
                session['token']=token
                msg = Message('Confirmation', sender = 'ishendrapratap2@gmail.com', recipients = [email])
                msg.body = "Use this token in change password:"+str(token)
                mail.send(msg)
                return jsonify("found")
            else:
                return jsonify("not found")    
        except:
            raise        
    return render_template("forget_password_email.html")

#check token is valid or not
@app.route("/change_password",methods=['GET','POST'])
def change_password():
    if request.method=='POST':
        token=request.form['token']
        token1=session['token']
        if str(token)==str(token1):
            return jsonify("Matched")
        else:
            return jsonify("Not Matched")    
        
    return render_template("forget_password.html")
    
#Update password controller
@app.route("/update_password",methods=['GET','POST'])
def update_password():
    if request.method=='POST':
        password=request.form['password']
        
        pwd=encrypt_string(password)
        query = """UPDATE registration
            SET password = %s
            WHERE email = %s """
        try:
            data = (pwd,session['email'])
            cur.execute(query, data)
            db.commit()
            return jsonify("done")
        except:
            raise
        return jsonify("done")

#Get selected variety details
@app.route("/variety",methods=['GET','POST'])
def get_variety():
   
    variety=request.form['variety']
    json_data1=session['json_data']
    for x in range(len(json_data1)):
        print (json_data1[x]['variety_name'])
        if json_data1[x]['variety_name']==variety:
            session['varietydetails']=json_data1[x]
            return jsonify(json_data1[x])

#show selected variety detail page
@app.route("/varietydetail",methods=['POST','GET'])
def variety_detail():
    print ('vareity details controller')
    y =session['varietydetails']
    return render_template("morevariety.html",crop=y,county=session['county'])

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
    app.register_error_handler(400, handle_bad_request)
