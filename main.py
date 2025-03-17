import os
import base64
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
#import algm
from datetime import datetime
from datetime import date
import datetime
import calendar
#from datetime import date, timedelta
import math
from flask_mail import Mail, Message
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

import random
from random import seed
from random import randint

from urllib.request import urlopen
import webbrowser

#import xlrd 
from flask import send_file
from werkzeug.utils import secure_filename
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  use_pure=True,
  database="eb_forecasting"

)

#from store import *


app = Flask(__name__)
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
##email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "rnd1024.64@gmail.com",
    "MAIL_PASSWORD": "kazxlklvfrvgncse"
}

app.config.update(mail_settings)
mail = Mail(app)
#######

@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    act = ""
    name=""
    mobile=""
    message=""
    ff=open("user.txt","w")
    ff.write("")
    ff.close()
        
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        

        cursor.execute('SELECT count(*) FROM eb_register WHERE uname = %s && train_st=1', (uname, ))
        cnt = cursor.fetchone()[0]
        if cnt>0:
        
            #cursor.execute('SELECT * FROM eb_register WHERE uname = %s && pass = %s', (uname, pwd))
            #account = cursor.fetchone()
            #username=account[10]
            #if account:
            ff2=open("uname.txt","w")
            ff2.write(uname)
            ff2.close()
            #print(ff2)
            otp=randint(1000,9999)
            ff=open("num.txt","w")
            ff.write(str(otp))
            ff.close()
            session['username'] = uname
            cursor.execute('SELECT * FROM eb_register WHERE uname = %s', (uname, ))
            dtt = cursor.fetchone()
            act='sms'
            name=dtt[1]
            mobile=dtt[6]
            message="OTP: "+str(otp)
            #return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg,act=act,message=message,mobile=mobile,name=name)


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    msg=""


    if request.method=='POST':
        key=request.form['otp']
       
        ff=open("num.txt","r")
        otp=ff.read()
        ff.close()
        if otp==key:
            return redirect(url_for('home'))
        else:
            msg="OTP wrong!"
            
    return render_template('verify_otp.html',msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()

        if uname=="admin":
            cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
            account = cursor.fetchone()
            if account:
                session['username'] = uname
                return redirect(url_for('view_data'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
        else:
            cursor.execute('SELECT * FROM eb_Staff WHERE uname = %s AND pass = %s', (uname, pwd))
            account = cursor.fetchone()
            if account:
                session['username'] = uname
                #now = datetime.datetime.now()
                now=date.today()
                rdate=now.strftime("%d-%m-%Y")
                ff=open("rdate.txt","w")
                ff.write(rdate)
                ff.close()
            
                return redirect(url_for('staff_home'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
    
        
        
    return render_template('login.html',msg=msg,act=act)

@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
    msg=""
    act = request.args.get('act')
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM eb_Staff WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            #now = datetime.datetime.now()
            now=date.today()
            rdate=now.strftime("%d-%m-%Y")
            ff=open("rdate.txt","w")
            ff.write(rdate)
            ff.close()
        
            return redirect(url_for('staff_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
        
        
    return render_template('login_staff.html',msg=msg,act=act)





@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register ")
    data = mycursor.fetchall()

    
    
    return render_template('admin.html', data=data)

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_staff ")
    data = mycursor.fetchall()


    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        area=request.form['area']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM eb_staff")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        cursor = mydb.cursor()
        sql = "INSERT INTO eb_staff(id,name,area,city,mobile,email,uname,pass) VALUES (%s,%s,%s,%s, %s, %s, %s, %s)"
        val = (maxid,name,area,city,mobile,email,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()

        message="Dear "+name+", Your Staff ID: "+uname+" ,Password: "+pass1
        #url="http://iotcloud.co.in/testmail/testmail1.php?email="+email+"&message="+message
        #webbrowser.open_new(url)
        with app.app_context():
            msg = Message(subject="EB Staff", sender=app.config.get("MAIL_USERNAME"),recipients=[email], body=message)
            mail.send(msg)
            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        
        if cursor.rowcount==1:
            return redirect(url_for('view_data'))
        else:
            
            msg='Already Exist'
            
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from eb_staff where id=%s",(did,))
        return redirect(url_for('staff'))
        
    return render_template('staff.html', msg=msg, data=data)


@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register ")
    data = mycursor.fetchall()
    
    return render_template('monitor.html', data=data)




@app.route('/usage', methods=['GET', 'POST'])
def usage():
    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT distinct(month) FROM eb_monitor order by month")
    data = mycursor.fetchall()

    
    mycursor.execute("SELECT distinct(year) FROM eb_monitor order by year desc")
    data2 = mycursor.fetchall()
        
    usage1=[]
    #mycursor = mydb.cursor()
    #mycursor.execute("SELECT * FROM eb_power")
    #usage = mycursor.fetchall()
    if request.method=='POST':
        month=request.form['month']
        year=request.form['year']
        mycursor.execute("SELECT * FROM eb_monitor where month=%s and year=%s",(month,year))
        usage1 = mycursor.fetchall()
    
    return render_template('usage.html', data=data,data2=data2,usage1=usage1)


@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register ")
    data = mycursor.fetchall()

    if request.method=='POST':
        name=request.form['name']
        ebno=request.form['ebno']
        address=request.form['address']
        city=request.form['city']
        area=request.form['area']
        mobile1=request.form['mobile']
        email=request.form['email']
        
        rdate=date.today()
        print(rdate)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM eb_register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        uname="C"+str(maxid) #request.form['uname']
        pass1="1234"#request.form['pass']
        
        now = date.today()
        rdate=now.strftime("%d-%m-%Y")
        cursor = mydb.cursor()
        sql = "INSERT INTO eb_register(id,name,ebno,address,area,city,mobile,email,uname,pass,rdate) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,ebno,address,area,city,mobile1,email,uname,pass1,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"

        message="Consumer: "+name+", EB No.:"+ebno+", Consumer ID:"+uname
        #url="http://iotcloud.co.in/testmail/sendmail.php?email="+email+"&message="+message
        #webbrowser.open_new(url)

        with app.app_context():
            msg = Message(subject="EB Consumer", sender=app.config.get("MAIL_USERNAME"),recipients=[email], body=message)
            mail.send(msg)
            
        if cursor.rowcount==1:
            return redirect(url_for('index',act='1'))
        else:
            return redirect(url_for('index',act='2'))
            #msg='Already Exist'  
    
    return render_template('view_user.html', data=data)


@app.route('/reg', methods=['GET', 'POST'])
def reg():

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register ")
    data = mycursor.fetchall()

    if request.method=='POST':
        uname=request.form['uname']
        pass1=request.form['pass']
        mycursor.execute("update eb_register set pass=%s where uname=%s",(pass1,uname))
        mydb.commit()
        return redirect(url_for('index',act='1'))
        
    return render_template('reg.html')

@app.route('/view_req', methods=['GET', 'POST'])
def view_req():
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register ")
    data = mycursor.fetchall()
    
    return render_template('view_req.html', data=data)




@app.route('/home', methods=['GET', 'POST'])
def home():
    uname=""
    if 'username' in session:
        uname = session['username']
    print(uname)
    #uname="C1"
    f5=open("uname.txt","r")
    uname=f5.read()
    f5.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register where uname=%s",(uname, ))
    account = mycursor.fetchone()

    now = date.today() #datetime.datetime.now()
    yr=now.strftime("%Y")
    mon=now.strftime("%m")
    mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
    dc = mycursor.fetchone()[0]
    if dc==0:
        i=1
        mycursor.execute("SELECT * FROM eb_device")
        edata =mycursor.fetchall()
        for ed in edata:
            mycursor.execute("SELECT max(id)+1 FROM eb_monitor")
            maxid1 = mycursor.fetchone()[0]
            if maxid1 is None:
                maxid1=1

            ed1=ed[0]
            sql2 = "INSERT INTO eb_monitor(id,uname,edevice,status,seconds,unit,month,year,device) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val2 = (maxid1,uname,ed1,0,0,0,mon,yr,ed[1])
            mycursor.execute(sql2, val2)
            mydb.commit()   
            i+=1

    
            

    #path = 'eb-data.csv'
    fn=uname+".csv"
    path='dataset/'+fn
    #df = pd.read_csv(path, header=0)
    df = pd.read_csv(path, header=0)
    
    data=[]
    for ss in df.values:
        data.append(ss)

    #print(data)
    datah=['Fan','Tubelight','Television','Refrigerator','Washing Mchine','Microwave Oven','Water Purifier','AC','Water Heater','Motor Pump','Air Cooler','Computer','Electric Stove']


    #print(data[0][1])

    #print(data[0])
    #print(data[12])
    #print(data[13])
    
    month = datetime.now().month
    print(month)

    gmon=0
    amon=['January','February','March','April','May','June','July','August','September','October','November','December']
    if month==12:
        gmon=0
    else:
        gmon=month


    nmonth=amon[gmon]

    tot=len(data)
    #print(data[0])
    n=0
    arr=[]
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0
    s8=0
    s9=0
    s10=0
    s11=0
    s12=0
    s13=0
    n=0
    for dd in data:
        
        if dd[3]==nmonth:
            j=2
            print(dd)
            s1+=dd[4]
            s2+=dd[5]
            s3+=dd[6]
            s4+=dd[7]
            s5+=dd[8]
            s6+=dd[9]
            s7+=dd[10]
            s8+=dd[11]
            s9+=dd[12]
            s10+=dd[13]
            s11+=dd[14]
            s12+=dd[15]
            s13+=dd[16]
            

            n+=1

    arr=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13]
    print("****")
    print(arr)
    
    val=[]
    vv=0
    i=0
    data3=[]

    mycursor.execute('delete from eb_predict')
    mydb.commit()
    
    for ds in arr:
        
        
        if ds>0:
            v1=ds/n
        
            vv=round(v1)
            val.append(vv)
        else:
            val.append(vv)
        
        dt=[]
        dt.append(datah[i])
        dt.append(str(vv))
        ###
        mycursor.execute("SELECT max(id)+1 FROM eb_predict")
        maxid1 = mycursor.fetchone()[0]
        if maxid1 is None:
            maxid1=1
        sql2 = "INSERT INTO eb_predict(id,edevice,eb_usage) VALUES (%s, %s, %s)"
        val2 = (maxid1,datah[i],str(vv))
        mycursor.execute(sql2, val2)
        mydb.commit()   
        ###
        data3.append(dt)
        i+=1

    ##########
    #pie--appliances
    bval=datah
     
    data = val #[23, 17, 35, 29, 12, 41]
     
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = bval)
     
    # show plot
    #plt.show()
    fn="graph6.png"
    plt.savefig('static/'+fn)
    plt.close()
    #############################################
    #print(val)
    #data3.sort(reverse=True)
    #print(data3)
    mycursor.execute("SELECT * FROM eb_predict order by eb_usage desc")
    data4 = mycursor.fetchall()
    ################################################

    #graph1   
    dd2=val

    #g1=100
    ax=dd2
    dd1=datah

    doc = dd1 #list(data.keys())
    values = dd2 #list(data.values())
      
    fig = plt.figure(figsize = (10, 5))

    c=['green','orange','yellow','red','brown','blue','pink','green','yellow','red','pink','blue','yellow']
    # creating the bar plot
    plt.bar(doc, values, color =c,
            width = 0.4)

    #plt.ylim((1,g1))

    plt.xlabel("Appliances")
    plt.ylabel("Energy Consumption")
    plt.title("")


    fn="graph1.png"
    plt.xticks(rotation=20)

    plt.savefig('static/'+fn)
    plt.close()
    #plt.clf()


    ############################################################################3333
    
    #graph2--year--forecast month

    mycursor.execute("SELECT * FROM eb_data where uname=%s and month=%s group by year",(uname,nmonth))
    data5 = mycursor.fetchall()

    arr_yr=[]
    arr_x=[]
    y=[]
    x1=[]
    x2=[]
    x3=[]
    for ss in data5:
        arr_yr.append(ss[2])
        sm=[ss[4],ss[5],ss[6],ss[7],ss[8],ss[9],ss[10],ss[11],ss[12],ss[13],ss[14],ss[15],ss[16]]
        #sm=ss[4]+ss[5]+ss[6]+ss[7]+ss[8]+ss[9]+ss[10]+ss[11]+ss[12]+ss[13]+ss[14]+ss[15]+ss[16]
        #smm=round(sm/13)
        arr_x.append(sm)
        
   

    x1=arr_x[0]
    x2=arr_x[1]
    x3=arr_x[2]
    
    
    #x1=arr_x
    #x2=[2,4,5,7,3]
    y=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    plt.plot(y,x3)
    dd=["",""]
    plt.legend(arr_yr)
    plt.xlabel("Appliances")
    plt.ylabel("Energy Consumption")
    
    fn="graph2.png"
    plt.savefig('static/'+fn)
    plt.close()
    ###############################################################
    ##pie
    arr_mn=[]
    arr_x=[]
    mycursor.execute("SELECT * FROM eb_data where uname=%s && year=%s group by month",(uname,yr))
    data6 = mycursor.fetchall()
    for ss in data6:
        ss1=str(ss[3])+" "+str(ss[2])
        arr_mn.append(ss1)
        sm=ss[4]+ss[5]+ss[6]+ss[7]+ss[8]+ss[9]+ss[10]+ss[11]+ss[12]+ss[13]+ss[14]+ss[15]+ss[16]
        smm=round(sm/13)
        arr_x.append(smm)
    
    #cars = ['AUDI', 'BMW', 'FORD',
    #        'TESLA', 'JAGUAR', 'MERCEDES']

    bval=arr_mn
     
    data = arr_x #[23, 17, 35, 29, 12, 41]
     
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = bval)
     
    # show plot
    #plt.show()
    fn="graph3.png"
    plt.savefig('static/'+fn)
    plt.close()

    #####  FORECASTING #####################################

    arr_mn=[]
    arr_x=[]
    mycursor.execute("SELECT * FROM eb_data where uname=%s && month=%s && year!=%s",(uname,nmonth,yr))
    data7 = mycursor.fetchall()
    for ss in data7:
        ss1=str(ss[3])+" "+str(ss[2])
        arr_mn.append(ss1)
        sm=ss[4]+ss[5]+ss[6]+ss[7]+ss[8]+ss[9]+ss[10]+ss[11]+ss[12]+ss[13]+ss[14]+ss[15]+ss[16]
        smm=round(sm/13)
        arr_x.append(smm)

    av=0
    nn=0
    predict=0
    for ax in arr_x:
        av+=ax
        nn+=1
    if av>0:
        predict=round(av/nn)

    arr_x.append(predict)

    cm=nmonth+" "+yr
    arr_mn.append(cm)
    
    dd2=arr_x

    t=len(arr_mn)

    #g1=100
    
    dd1=arr_mn
    print(dd1)
    doc=[]
    values=[]
    doc = dd1 #list(data.keys())
    values = dd2 #list(data.values())
      
    fig = plt.figure(figsize = (10, 5))

    ccc=['red','orange','yellow','green','brown','blue','pink','green','yellow','red','pink','blue','yellow']
    c=[]
    j=0
    while j<t:
        n2=randint(0,11)
        ccc1=ccc[n2]
        c.append(ccc1)
        j+=1
    # creating the bar plot
    plt.bar(doc, values, color =c, width = 0.4)

    #plt.ylim((1,g1))

    plt.xlabel("Year")
    plt.ylabel("Energy Consumption")
    plt.title("")
    
    fn="graph4.png"
    plt.savefig('static/'+fn)
    plt.close()    

    #############################################
    #pie--3 yr
    arr_mn=[]
    arr_x=[]
    mycursor.execute("SELECT * FROM eb_data where uname=%s && month=%s",(uname,nmonth))
    data6 = mycursor.fetchall()
    for ss in data6:
        ss1=str(ss[3])+" "+str(ss[2])
        arr_mn.append(ss1)
        sm=ss[4]+ss[5]+ss[6]+ss[7]+ss[8]+ss[9]+ss[10]+ss[11]+ss[12]+ss[13]+ss[14]+ss[15]+ss[16]
        smm=round(sm/13)
        arr_x.append(smm)
    
    #cars = ['AUDI', 'BMW', 'FORD',
    #        'TESLA', 'JAGUAR', 'MERCEDES']

    bval=arr_mn
     
    data = arr_x #[23, 17, 35, 29, 12, 41]
     
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = bval)
     
    # show plot
    #plt.show()
    fn="graph5.png"
    plt.savefig('static/'+fn)
    plt.close()
    ############################################
    
    
    '''
    j=0
    n=0
    dtt=[]
    while j<tot:
        mm=data[j][1]
        if mm==nmonth:
            dtt.append(data[j])
            n+=1 
            
        j+=1

    print(dtt)

    vv=[]
    for dss in dtt:
        i=2
        a1=[]
        aa=0
        while i<=14:
            gsum=0
            aa=a1[i]
            aa+=dss[i]
            a1.append(aa)
            
            i+=1
    '''
    ###################
     
    
    '''m1=gmon
    m2=m1+12
    m3=m1+24

    print(data[m1])
    print(data[m2])
    print(data[m3])

    i=2
    
    dt=[]
    while i<=14:
        gsum=0
        a1=data[m1][i]
        a2=data[m2][i]
        a3=data[m3][i]
        gsum=a1+a2+a3
        gsum1=gsum/3
        v=round(gsum1)
        dt.append(v)
        
        i+=1

    print("----")
    print(dt)'''
    ###################

    
    #numbers=dt
    #numbers.sort(reverse = True)
    #print(numbers)
    
    return render_template('home.html', account=account,uname=uname,nmonth=nmonth,data4=data4,yr=yr)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        ebno=request.form['ebno']
        address=request.form['address']
        city=request.form['city']
        area=request.form['area']
        mobile1=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        rdate=date.today()
        print(rdate)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM eb_register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today()
        rdate=now.strftime("%d-%m-%Y")
        cursor = mydb.cursor()
        sql = "INSERT INTO eb_register(id,name,ebno,address,area,city,mobile,email,uname,pass,rdate) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,ebno,address,area,city,mobile1,email,uname,pass1,rdate)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        
        if cursor.rowcount==1:
            return redirect(url_for('index',act='1'))
        else:
            return redirect(url_for('index',act='2'))
            #msg='Already Exist'  
    return render_template('register.html',msg=msg)

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    msg=""
    if request.method=='POST':
        name=request.form['name']
        city=request.form['city']
        area=request.form['area']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM eb_staff")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        cursor = mydb.cursor()
        sql = "INSERT INTO eb_staff(id,name,area,city,mobile,email,uname,pass) VALUES (%s,%s,%s,%s, %s, %s, %s, %s)"
        val = (maxid,name,area,city,mobile,email,uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        
        if cursor.rowcount==1:
            return redirect(url_for('view_staff'))
        else:
            
            msg='Already Exist'  
    return render_template('add_staff.html',msg=msg)

   
@app.route('/set_limit', methods=['GET', 'POST'])
def set_limit():
    data=""
    msg=""
    if 'username' in session:
        uname = session['username']

    f5=open("uname.txt","r")
    uname=f5.read()
    f5.close()
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register where uname=%s",(uname, ))
    data = mycursor.fetchone()
    if request.method=='POST':
        limit=request.form['setlimit']
        d1=request.form['d1']
        d2=request.form['d2']
        d3=request.form['d3']
        d4=request.form['d4']
        d5=request.form['d5']
        d6=request.form['d6']
        d7=request.form['d7']
        d8=request.form['d8']
        d9=request.form['d9']
        d10=request.form['d10']
        d11=request.form['d11']
        d12=request.form['d12']
        d13=request.form['d13']
        

        mycursor.execute("SELECT * FROM eb_register where uname=%s",(uname, ))
        data1 = mycursor.fetchone()
        
        
        mycursor.execute("update eb_register set setlimit=%s,d1=%s,d2=%s,d3=%s,d4=%s,d5=%s,d6=%s,d7=%s,d8=%s,d9=%s,d10=%s,d11=%s,d12=%s,d13=%s where uname=%s",(limit,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,uname))
        mydb.commit()

       
        
        msg="success"
        return redirect(url_for('set_limit',msg=msg))

    ##    
    
    return render_template('set_limit.html',uname=uname,data=data)




@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    data=""
    
    account=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_device")
    val = mycursor.fetchall()
##    if request.method=='GET':
##        act = request.args.get('edevice')
##        print(act)
##        mycursor = mydb.cursor()
##        mycursor.execute("SELECT * FROM eb_device where device=%s",(act, ))
##        account = mycursor.fetchone()
##    print(account)
    if request.method=='POST':
        edevice=request.form['gid[]']
        mycursor = mydb.cursor()
        sql=("update eb_register set edevice=%s where uname=%s ")
        val=(edevice,data)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"
        return redirect(url_for('add_device',msg=msg,edevice=edevice))
    
   
    return render_template('add_device.html', data=data,val=val,account=account)





@app.route('/monitor3', methods=['GET', 'POST'])
def monitor3():
    data=""
    uname=""
    did=0
    st=0
    dc1=0
    dc2=0
    if 'username' in session:
        uname = session['username']

    f5=open("uname.txt","r")
    uname=f5.read()
    f5.close()
    #uname='C1'    
    mycursor = mydb.cursor()
    

    now = date.today()
    yr=now.strftime("%Y")
    mon=now.strftime("%m")
    rdate=now.strftime("%d-%m-%Y")

    mycursor.execute("SELECT * FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
    data = mycursor.fetchall()

    fmonth=""
    print(mon)
    tdays=0
    if mon=="01":
        tdays=31
        fmonth="January"
    elif mon=="02":
        yrr=int(yr)
        if yrr%4==0:
            tdays=29
        else:
            tdays=28
        fmonth="February"
    elif mon=="03":
        tdays=31
        fmonth="March"
    elif mon=="04":
        tdays=30
        fmonth="April"
    elif mon=="05":
        tdays=31
        fmonth="May"
    elif mon=="06":
        tdays=30
        fmonth="June"
    elif mon=="07":
        tdays=31
        fmonth="July"
    elif mon=="08":
        tdays=31
        fmonth="August"
    elif mon=="09":
        tdays=30
        fmonth="September"
    elif mon=="10":
        tdays=31
        fmonth="October"
    elif mon=="11":
        tdays=30
        fmonth="November"
    elif mon=="12":
        tdays=31
        fmonth="December"

    i=1
    data3=[]
    while i<=tdays:
        dt=[]
        dd=""
        if i<10:
            dd='0'+str(i)
        else:
            dd=str(i)
        dd1=dd+"-"+mon+"-"+yr
        dt.append(dd1)

        mycursor.execute("SELECT count(*) FROM eb_unit where uname=%s and rdate=%s",(uname,dd1))
        cnt = mycursor.fetchone()[0]
        if cnt>0:
            mycursor.execute("SELECT * FROM eb_unit where uname=%s and rdate=%s",(uname,dd1))
            cdd = mycursor.fetchone()
            if cdd[5]==dd1:
                dt.append(cdd[3])
            
        
            
        data3.append(dt)
        i+=1
    print(data3)
    ###export data#####################################

    mycursor.execute("SELECT count(*) FROM eb_data where uname=%s and month=%s and year=%s",(uname,fmonth,yr))
    cn = mycursor.fetchone()[0]

    if cn==0:
        mycursor.execute("SELECT * FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
        data5 = mycursor.fetchall()
        dt5=[]
        for d5 in data5:
            uv=round(d5[5])
            dt5.append(uv)

        mycursor.execute("SELECT max(id)+1 FROM eb_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        
        sql = "INSERT INTO eb_data(id,uname,year,month,fan,tubelight,television,refrigerator,washing_machine,microwave_ovan,water_purifier,ac,water_heater,motor_pump,air_cooler,computer,electric_stove) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,yr,fmonth,dt5[0],dt5[1],dt5[2],dt5[3],dt5[4],dt5[5],dt5[6],dt5[7],dt5[8],dt5[9],dt5[10],dt5[11],dt5[12])
        mycursor.execute(sql, val)
        mydb.commit()            
        
        mycursor.execute("SELECT * FROM eb_data where uname=%s",(uname,))
        result = mycursor.fetchall()
        fn=uname+".csv"
        with open('dataset/'+fn,'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in mycursor.description)
            for row in result:
                writer.writerow(row)

        with open('dataset/'+fn) as input, open('dataset/'+fn, 'w', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in mycursor.description)
            for row in result:
                if row or any(row) or any(field.strip() for field in row):
                    writer.writerow(row)

    else:
        mycursor.execute("SELECT * FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
        data5 = mycursor.fetchall()
        dt5=[]
        for d5 in data5:
            uv=round(d5[5])
            dt5.append(uv)
            
        sql="update eb_data set fan=%s,tubelight=%s,television=%s,refrigerator=%s,washing_machine=%s,microwave_ovan=%s,water_purifier=%s,ac=%s,water_heater=%s,motor_pump=%s,air_cooler=%s,computer=%s,electric_stove=%s where uname=%s and month=%s and year=%s"
        val=(dt5[0],dt5[1],dt5[2],dt5[3],dt5[4],dt5[5],dt5[6],dt5[7],dt5[8],dt5[9],dt5[10],dt5[11],dt5[12],uname,fmonth,yr)
        mycursor.execute(sql,val)
        mydb.commit()

        mycursor.execute("SELECT * FROM eb_data where uname=%s",(uname,))
        result = mycursor.fetchall()
        fn=uname+".csv"
        with open('dataset/'+fn,'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in mycursor.description)
            for row in result:
                writer.writerow(row)

        with open('dataset/'+fn) as input, open('dataset/'+fn, 'w', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in mycursor.description)
            for row in result:
                if row or any(row) or any(field.strip() for field in row):
                    writer.writerow(row)
        
            

    
        
    ##################################33
    
    if request.method=='GET':
        act = request.args.get('act')
        did = request.args.get('did')
        if did is None:
            did=0
        else:
            did=int(did)
        if act=="ON":
            st=1
        else:
            st=0
        '''    
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=%s",(uname,mon,yr,did))
        dc = mycursor.fetchone()[0]
        if dc>0:
            mycursor.execute("update eb_monitor set status=%s where uname=%s and month=%s and year=%s and edevice=%s",(st,uname,mon,yr,did))
            mydb.commit()
         


        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=1",(uname,mon,yr))
        dc1 = mycursor.fetchone()[0]
        if dc1 is None:
            dc1=0
        
        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=2",(uname,mon,yr))
        dc2 = mycursor.fetchone()[0]
        if dc2 is None:
            dc2=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=3",(uname,mon,yr))
        dc3 = mycursor.fetchone()[0]
        if dc3 is None:
            dc3=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=4",(uname,mon,yr))
        dc4 = mycursor.fetchone()[0]
        if dc4 is None:
            dc4=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=5",(uname,mon,yr))
        dc5 = mycursor.fetchone()[0]
        if dc5 is None:
            dc5=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=6",(uname,mon,yr))
        dc6 = mycursor.fetchone()[0]
        if dc6 is None:
            dc6=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=7",(uname,mon,yr))
        dc7 = mycursor.fetchone()[0]
        if dc7 is None:
            dc7=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=8",(uname,mon,yr))
        dc8 = mycursor.fetchone()[0]
        if dc8 is None:
            dc8=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=9",(uname,mon,yr))
        dc9 = mycursor.fetchone()[0]
        if dc9 is None:
            dc9=0

        mycursor.execute("SELECT status FROM eb_monitor where uname=%s and month=%s and year=%s and edevice=10",(uname,mon,yr))
        dc10 = mycursor.fetchone()[0]
        if dc10 is None:
            dc10=0
        '''
    #,dc1=dc1,dc2=dc2,dc3=dc3,dc4=dc4,dc5=dc5,dc6=dc6,dc7=dc7,dc8=dc8,dc9=dc9,dc10=dc10



    return render_template('monitor2.html', data=data,data3=data3)

@app.route('/load_unit', methods=['GET', 'POST'])
def load_unit():
    msg=""
    msg1=""
    msg2=""
    msg3=""
    msg4=""
    msg5=""
    msg6=""
    msg7=""
    msg8=""
    msg9=""
    msg10=""
    msg11=""
    msg12=""
    msg13=""
    uname=""
    if 'username' in session:
        uname = session['username']

    f5=open("uname.txt","r")
    uname=f5.read()
    f5.close()

    #try:

    now = date.today() #datetime.datetime.now()
    yr=now.strftime("%Y")
    mon=now.strftime("%m")

    rdate=now.strftime("%d-%m-%Y")
    
    uu=0
    uu2=0
    dd2=0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register where uname=%s",(uname,))
    dds1 = mycursor.fetchone()
    name=dds1[1]
    # and status=1

    rn1=randint(1,13)
    rn2=randint(1,13)
    rn3=randint(1,13)

    mycursor.execute("SELECT * FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
    dd1 = mycursor.fetchall()
    i=1
    for rr1 in dd1:
        if rn1==i:
            print(rn1)
            print(rr1[0])
            mycursor.execute("update eb_monitor set seconds=seconds+15 where uname=%s and month=%s and year=%s && id=%s",(uname,mon,yr,rr1[0]))
            mydb.commit()
        if rn2==i:
            mycursor.execute("update eb_monitor set seconds=seconds+15 where uname=%s and month=%s and year=%s && id=%s",(uname,mon,yr,rr1[0]))
            mydb.commit()
        if rn3==i:
            mycursor.execute("update eb_monitor set seconds=seconds+15 where uname=%s and month=%s and year=%s && id=%s",(uname,mon,yr,rr1[0]))
            mydb.commit()
        i+=1

    
    
    mycursor.execute("SELECT * FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
    dd = mycursor.fetchall()
    for rr in dd:

        
        mycursor.execute("SELECT * FROM eb_device where id=%s",(rr[2], ))
        dd2 = mycursor.fetchone()
        print(dd2[2])
        #unit=dd2[2]
        unit=0.5
        sec=rr[4]
        if sec>0:
            uu=sec/20
            uu2=uu*unit
            print(str(sec)+" "+str(unit)+" = "+str(uu2))
            mycursor.execute("update eb_monitor set unit=%s where uname=%s and month=%s and year=%s and edevice=%s",(uu2,uname,mon,yr,rr[2]))
            mydb.commit()

    ####
            
    mycursor.execute("SELECT count(*) FROM eb_unit where uname=%s and rdate=%s",(uname,rdate))
    dcnt = mycursor.fetchone()[0]
    if dcnt>0:
        sn=0
        su=0
        # and status=1
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s",(uname,))
        sr11 = mycursor.fetchone()[0]
        if sr11>0:
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s",(uname,))
            sr1 = mycursor.fetchall()
            for sr2 in sr1:
                sn+=1
                su+=0.25
            if sn>0:
                mycursor.execute("update eb_unit set seconds=seconds+5 where uname=%s && rdate=%s",(uname,rdate))
                mydb.commit()

                #mycursor.execute("SELECT sum(seconds) FROM eb_unit where uname=%s and rdate=%s",(uname,rdate))
                #drr = mycursor.fetchone()[0]
                #if drr>20:
                #    sec=drr/20
                #    sec1=float(sec)
                #    unit=0.5
                sec1=0.25
                uu_unit=sec1*su
                mycursor.execute("update eb_unit set unit=unit+%s where uname=%s && rdate=%s",(uu_unit,uname,rdate))
                mydb.commit()
        
    else:

        mycursor.execute("SELECT max(id)+1 FROM eb_unit")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO eb_unit(id,uname,seconds,unit,rdate,status,month,year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,'5','0',rdate,'0',mon,yr)
        mycursor.execute(sql, val)
        mydb.commit()      
    #############################
            
    #mycursor.execute("SELECT sum(unit) FROM eb_monitor where uname=%s and month=%s and year=%s",(uname,mon,yr))
    #dd2 = mycursor.fetchone()[0]

    mycursor.execute("SELECT sum(unit) FROM eb_unit where uname=%s and status=0",(uname,))
    dd2 = mycursor.fetchone()[0]

    mycursor.execute("update eb_register set tot_unit=%s where uname=%s",(dd2,uname))

    mycursor.execute("SELECT count(*) FROM eb_register where uname=%s and status=0",(uname,))
    c1 = mycursor.fetchone()[0]

    if c1>0:
        mycursor.execute("SELECT * FROM eb_register where uname=%s and status=0",(uname,))
        dd3 = mycursor.fetchone()
        
        name=dd3[1]
        mobile=dd3[6]
        if dd3[13]>dd3[9]:
            msg="Over the Limit"
            mycursor.execute("update eb_register set status=1 where uname=%s",(uname,))
            mess="EB, Over the Limit"
            url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
            webbrowser.open_new(url)

    ###appli--over limit
    mycursor.execute("SELECT * FROM eb_register where uname=%s",(uname,))
    ud1 = mycursor.fetchone()
    mobile=ud1[6]
    dv1=ud1[16]
    
    dv2=ud1[17]
    dv3=ud1[18]
    dv4=ud1[19]
    dv5=ud1[20]
    dv6=ud1[21]
    dv7=ud1[22]
    dv8=ud1[23]
    dv9=ud1[24]
    dv10=ud1[25]
    print("=aa==========")
    print(dv10)
    print("*********")
    dv11=ud1[26]
    dv12=ud1[27]
    dv13=ud1[28]
    
    
    mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s",(uname,mon,yr))
    ad11 = mycursor.fetchone()[0]
    
    if ad11>0:
        
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=1 && alert_st=0",(uname,mon,yr))
        an1 = mycursor.fetchone()[0]
        if an1>0:
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=1 && alert_st=0",(uname,mon,yr))
            ad1 = mycursor.fetchone()
            print(ad1)
            ut1=ad1[5]
            
            if ut1>=dv1:
                msg1="Over usage in Fan"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=1",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg1+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=2 && alert_st=0",(uname,mon,yr))
        an2 = mycursor.fetchone()[0]
        if an2>0:
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=2 && alert_st=0",(uname,mon,yr))
            ad2 = mycursor.fetchone()
            ut2=ad2[5]
            if ut2>=dv2:
                msg2="Over usage in Tubelight"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=2",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg2+"&mobile="+str(mobile)
                webbrowser.open_new(url)

        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=3 && alert_st=0",(uname,mon,yr))
        an3 = mycursor.fetchone()[0]
        if an3>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=3 && alert_st=0",(uname,mon,yr))
            ad3 = mycursor.fetchone()
            ut3=ad3[5]
            if ut3>=dv3:
                msg3="Over usage in Television"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=3",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg3+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=4&& alert_st=0",(uname,mon,yr))
        an4 = mycursor.fetchone()[0]
        if an4>0: 
            mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=4 && alert_st=0",(uname,mon,yr))
            ad4 = mycursor.fetchone()
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=4 && alert_st=0",(uname,mon,yr))
            ad4 = mycursor.fetchone()
            ut4=ad4[5]
            if ut4>=dv4:
                msg4="Over usage in Refrigerator"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=4",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg4+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=5 && alert_st=0",(uname,mon,yr))
        an5 = mycursor.fetchone()[0]
        if an5>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=5 && alert_st=0",(uname,mon,yr))
            ad5 = mycursor.fetchone()
            ut5=ad5[5]
            if ut5>=dv5:
                msg5="Over usage in Washing Mchine"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=5",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg5+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=6 && alert_st=0",(uname,mon,yr))
        an6 = mycursor.fetchone()[0]
        if an6>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=6 && alert_st=0",(uname,mon,yr))
            ad6 = mycursor.fetchone()
            ut6=ad6[5]
            if ut6>=dv6:
                msg6="Over usage in Microwave Oven"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=6",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg6+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=7 && alert_st=0",(uname,mon,yr))
        an7 = mycursor.fetchone()[0]
        if an7>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=7 && alert_st=0",(uname,mon,yr))
            ad7 = mycursor.fetchone()
            ut7=ad7[5]
            if ut7>=dv7:
                msg7="Over usage in Water Purifier"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=7",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg7+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=8 && alert_st=0",(uname,mon,yr))
        an8 = mycursor.fetchone()[0]
        if an8>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=8 && alert_st=0",(uname,mon,yr))
            ad8 = mycursor.fetchone()
            ut8=ad8[5]
            if ut8>=dv8:
                msg8="Over usage in AC"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=8",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg8+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=9 && alert_st=0",(uname,mon,yr))
        an9 = mycursor.fetchone()[0]
        if an9>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=9 && alert_st=0",(uname,mon,yr))
            ad9 = mycursor.fetchone()
            ut9=ad9[5]
            if ut9>=dv9:
                msg9="Over usage in Water Heater"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=9",(uname,mon,yr))
                mydb.commit()
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg9+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=10 && alert_st=0",(uname,mon,yr))
        an10 = mycursor.fetchone()[0]
        if an10>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=10 && alert_st=0",(uname,mon,yr))
            ad10 = mycursor.fetchone()
            ut10=ad10[5]
            print("=======")
            print(ut10)
            print("********")
            if ut10>=dv10:
                msg10="Over usage in Motor Pump"
                print(msg10)
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=10",(uname,mon,yr))
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg10+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=11 && alert_st=0",(uname,mon,yr))
        an11 = mycursor.fetchone()[0]
        if an11>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=11 && alert_st=0",(uname,mon,yr))
            ad11 = mycursor.fetchone()
            ut11=ad11[5]
            if ut11>=dv11:
                msg11="Over usage in Air Cooler"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=11",(uname,mon,yr))
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg11+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=12 && alert_st=0",(uname,mon,yr))
        an12 = mycursor.fetchone()[0]
        if an12>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=12 && alert_st=0",(uname,mon,yr))
            ad12 = mycursor.fetchone()
            ut12=ad12[5]
            if ut12>=dv12:
                msg12="Over usage in Computer"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=12",(uname,mon,yr))
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg12+"&mobile="+str(mobile)
                webbrowser.open_new(url)
        ##
        mycursor.execute("SELECT count(*) FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=13 && alert_st=0",(uname,mon,yr))
        an13 = mycursor.fetchone()[0]
        if an13>0: 
            mycursor.execute("SELECT * FROM eb_monitor where uname=%s && month=%s && year=%s && edevice=13 && alert_st=0",(uname,mon,yr))
            ad13 = mycursor.fetchone()
            ut13=ad13[5]
            if ut13>=dv13:
                msg13="Over usage in Electric Stove"
                mycursor.execute("update eb_monitor set alert_st=1 where uname=%s && month=%s && year=%s && edevice=13",(uname,mon,yr))
                url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+msg13+"&mobile="+str(mobile)
                webbrowser.open_new(url)
                
        
    #except:
    #    print("try")
        
        
    return render_template('load_unit.html',data=dd2,msg=msg,msg1=msg1,msg2=msg2,msg3=msg3,msg4=msg4,msg5=msg5,msg6=msg6,msg7=msg7,msg8=msg8,msg9=msg9,msg10=msg10,msg11=msg11,msg12=msg12,msg13=msg13)

@app.route('/usage2', methods=['GET', 'POST'])
def usage2():
    data=""
    usage=""
    if 'username' in session:
        uname = session['username']
    bid=request.args.get("bid")
    mycursor = mydb.cursor()
    #mycursor.execute("SELECT distinct(month) FROM eb_monitor order by month")
    #data = mycursor.fetchall()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT distinct(year) FROM eb_monitor order by year desc")
    data2 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM eb_bill where uname=%s",(uname, ))
    data = mycursor.fetchall()
        
    usage1=[]
    #mycursor = mydb.cursor()
    #mycursor.execute("SELECT * FROM eb_power")
    #usage = mycursor.fetchall()
    if request.method=='POST':
        month=request.form['month']
        year=request.form['year']
        mycursor.execute("SELECT * FROM eb_monitor where month=%s and year=%s",(month,year))
        usage1 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM eb_bill b,eb_register r where b.uname=r.uname && b.id=%s",(bid, ))
    data1 = mycursor.fetchone()
    
    return render_template('usage2.html',uname=uname, data=data,data1=data1)


@app.route('/user_req', methods=['GET', 'POST'])
def user_req():
    data=""
    if 'username' in session:
        uname = session['username']
    user_req=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_power")
    power = mycursor.fetchall()
    if request.method=='POST':
        month=request.form['month']
        year=request.form['year']
        today = date.today()
        rdate = today.strftime("%b-%d-%Y")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM eb_request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        cursor = mydb.cursor()
        sql = "INSERT INTO eb_request(id,uname,month,year,rdate,status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,data,month,year,rdate,'0')
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        mycursor.execute("SELECT * FROM eb_request")
        user_req = mycursor.fetchall()
    return render_template('user_req.html', data=data,power=power,user_req=user_req)

@app.route('/bill', methods=['GET', 'POST'])
def bill():
    data=""
    f1=open("uname.txt","r")
    data=f1.read()
    f1.close()
    
    return render_template('bill.html', data=data)



@app.route('/bill2', methods=['GET', 'POST'])
def bill2():
    data=""
    f1=open("uname.txt","r")
    data=f1.read()
    f1.close()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register where uname=%s",(data,))
    account = mycursor.fetchall()
    if request.method=='GET':
        billid=request.args.get('id')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM eb_power where id=%s",(billid,))
        power = mycursor.fetchall()
        
    return render_template('bill2.html', data=data,account=account,power=power)


@app.route('/staff_home', methods=['GET', 'POST'])
def staff_home():
    act=""
    if 'username' in session:
        uname = session['username']
    value=[]
    mycursor = mydb.cursor()
    
    uid=""
    if request.method=='POST':
        
        ebno = request.form['ebno']
        mycursor.execute("SELECT * FROM eb_register where ebno=%s",(ebno, ))
        value = mycursor.fetchall()
        uid=value[0][10]
        act="1"
        
    
    return render_template('staff_home.html', value=value,act=act,uid=uid)

from datetime import datetime, timedelta
def date_range(start, end):
            delta = end - start  # as timedelta
            days = [start + timedelta(days=i) for i in range(delta.days + 1)]
            return days
        
@app.route('/get_bill', methods=['GET', 'POST'])
def get_bill():

    
    act=""
    uid = request.args.get('uid')
    if 'username' in session:
        uname = session['username']
    value=[]
    unit=0
    amt=0
    uu=0
    sdate=""
    edate=""
    data=[]
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM eb_register where id=%s",(uid, ))
    udata = mycursor.fetchone()
    uname=udata[10]

    if request.method=='POST':
        
        sd = request.form['sdate']
        ed = request.form['edate']

        sdd=sd.split('-')
        sdate=sdd[2]+"-"+sdd[1]+"-"+sdd[0]

        edd=ed.split('-')
        edate=edd[2]+"-"+edd[1]+"-"+edd[0]

        print(sdate)
        print(edate)

        ###
        

        start_date = datetime(int(sdd[0]), int(sdd[1]), int(sdd[2]))
        end_date = datetime(int(edd[0]), int(edd[1]), int(edd[2]))
            
        dr=date_range(start_date, end_date)
        gdate=[]
        for drr in dr:
            date_time = drr.strftime("%d-%m-%Y")
            #print(date_time)
            gdate.append(date_time)
            '''ds2=ds1[1].split(',')

            if ds2[2]<10:
                dy="0"+ds2[2]
            else:
                dy=ds2[2]
            if ds2[1]<10:
                mn="0"+ds2[1]
            else:
                mn=ds2[1]

            gdd=dy+"-"+mn+"-"+yr
            gdate.append(gdd)'''


        print(gdate)
        
        for dty in gdate:
            dt=[]
            mycursor.execute("SELECT count(*) FROM eb_unit where uname=%s && rdate=%s",(uname,dty ))
            cdy = mycursor.fetchone()[0]
            
            if cdy>0:
                mycursor.execute("SELECT * FROM eb_unit where uname=%s && rdate=%s",(uname,dty ))
                cdd = mycursor.fetchone()
                print(cdd[3])
                unit+=cdd[3]
                dt.append(dty)
                dt.append(cdd[3])
                data.append(dt)   
        print(data)
        mycursor.execute("SELECT * FROM admin")
        am_det = mycursor.fetchone()
        if unit>=500:
            uu=unit*am_det[5]
        elif unit>=300:
            uu=unit*am_det[4]
        elif unit>=100:
            uu=unit*am_det[3]
        else:
            uu=unit*am_det[2]
        
        act="1"
        amt=uu
        
                    
        
    
    return render_template('get_bill.html', value=value,uname=uname,act=act,data=data,uid=uid,sdate=sdate,edate=edate)


@app.route('/send', methods=['GET', 'POST'])
def send():

    
    act="1"
    uid = request.args.get('uid')
    sdate = request.args.get('sdate')
    edate = request.args.get('edate')
    
    if 'username' in session:
        uname = session['username']
    value=[]
    unit=0
    amt=0
    uu=0
    
    data=[]
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM eb_register where id=%s",(uid, ))
    udata = mycursor.fetchone()
    uname=udata[10]
    name=udata[1]
    mobile=udata[6]

    if act=="1":
        #sd = request.form['sdate']
        #ed = request.form['edate']

        sdd=sdate.split('-')
        
        print(sdd)
        #sdate=sdd[2]+"-"+sdd[1]+"-"+sdd[0]

        edd=edate.split('-')
        #edate=edd[2]+"-"+edd[1]+"-"+edd[0]

        print(sdate)
        print(edate)

        ###
            

        start_date = datetime(int(sdd[2]), int(sdd[1]), int(sdd[0]))
        end_date = datetime(int(edd[2]), int(edd[1]), int(edd[0]))
                
        dr=date_range(start_date, end_date)
        gdate=[]
        for drr in dr:
            date_time = drr.strftime("%d-%m-%Y")
            #print(date_time)
            gdate.append(date_time)
            
        #print(gdate)
        
        for dty in gdate:
            dt=[]
            mycursor.execute("SELECT count(*) FROM eb_unit where uname=%s && rdate=%s",(uname,dty ))
            cdy = mycursor.fetchone()[0]
            
            if cdy>0:
                mycursor.execute("SELECT * FROM eb_unit where uname=%s && rdate=%s",(uname,dty ))
                cdd = mycursor.fetchone()
                mycursor.execute("update eb_unit set status=1 where uname=%s && rdate=%s",(uname,dty ))
                
                unit+=cdd[3]
                dt.append(dty)
                dt.append(cdd[3])
                data.append(dt)   
        
        if unit>100:
            uu=unit*2
        else:
            uu=unit*1
        act="1"
        
        amt=math.ceil(uu)
        
        ff=open("rdate.txt","r")
        rdate=ff.read()
        ff.close()
        
        mycursor.execute("SELECT max(id)+1 FROM eb_bill")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        
        sql = "INSERT INTO eb_bill(id,uname,sdate,edate,unit,amount,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,sdate,edate,unit,amt,rdate)
        mycursor.execute(sql, val)
        mydb.commit()


        mycursor.execute("update eb_register set tot_unit=0,status=0 where uname=%s",(uname,))
        
        mess="EB Bill: Rs."+str(amt)
        url="http://iotcloud.co.in/testsms/sms.php?sms=msg&name="+name+"&mess="+mess+"&mobile="+str(mobile)
        webbrowser.open_new(url)
        #return redirect(url_for('staff_bill',uid=uname))             
        
    
    return render_template('send.html', value=value,act=act,data=data,uid=uid,sdate=sdate,edate=edate,uname=uname)


@app.route('/staff_bill', methods=['GET', 'POST'])
def staff_bill():
    uid = request.args.get('uid')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM eb_bill where uname=%s",(uid, ))
    data = mycursor.fetchall()
    

    
    return render_template('staff_bill.html',data=data)

@app.route('/ebbill', methods=['GET', 'POST'])
def ebbill():
    bid = request.args.get('bid')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM eb_bill b,eb_register r where b.uname=r.uname && b.id=%s",(bid, ))
    data = mycursor.fetchone()
    

    
    return render_template('ebbill.html',data=data)

@app.route('/add_amount', methods=['GET', 'POST'])
def add_amount():
    
    act=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM admin")
    data = mycursor.fetchone()
    
    
    if request.method=='POST':
        level1 = request.form['level1']
        level2 = request.form['level2']
        level3 = request.form['level3']
        level4 = request.form['level4']
        mycursor.execute("update admin set level1=%s,level2=%s,level3=%s,level4=%s  where username='admin'",(level1,level2,level3,level4))
        mydb.commit()

        return redirect(url_for('add_amount',act='yes')) 
    
    return render_template('add_amount.html',data=data,act=act)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    
    if request.method=='POST':
        
        #file = request.files['file']
        #try:
        #if file.filename == '':
        #    flash('No selected file')
        #    return redirect(request.url)
        #if file:
        #    fn="datafile.csv"
            #fn1 = secure_filename(fn)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
        return redirect(url_for('view_data'))
        #except:
        #    print("dd")
    return render_template('upload.html',msg=msg)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    uname=""
    act=request.args.get("act")
    mess=request.args.get("mess")
    user=""
    if 'username' in session:
        uname = session['username']
    '''filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        data.append(ss)
    cols=cnt
    if request.method=='POST':
        return redirect(url_for('preprocess'))'''

    #,data=data, msg=msg, rows=rows, cols=cols

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register")
    cdata = mycursor.fetchall()
    
    if request.method=='POST':
        user = request.form['user']
        month = request.form['month']
        year = request.form['year']
        fan = request.form['fan']
        tubelight = request.form['tubelight']
        television = request.form['television']
        refrigerator = request.form['refrigerator']
        washing_machine = request.form['washing_machine']
        microwave_ovan = request.form['microwave_ovan']
        water_purifier = request.form['water_purifier']
        ac = request.form['ac']
        water_heater = request.form['water_heater']
        motor_pump = request.form['motor_pump']
        air_cooler = request.form['air_cooler']
        computer = request.form['computer']
        electric_stove = request.form['electric_stove']

        mycursor.execute("SELECT count(*) FROM eb_data where uname=%s && year=%s && month=%s",(user,year,month))
        cu = mycursor.fetchone()[0]
        if cu==0:
        
            mycursor.execute("SELECT max(id)+1 FROM eb_data")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            uname="C"+str(maxid) #request.form['uname']
            pass1="1234"#request.form['pass']
            
            now = date.today()
            rdate=now.strftime("%d-%m-%Y")


            ff=open("user.txt","w")
            ff.write(user)
            ff.close()
            
            sql = "INSERT INTO eb_data(id,uname,year,month,fan,tubelight,television,refrigerator,washing_machine,microwave_ovan,water_purifier,ac,water_heater,motor_pump,air_cooler,computer,electric_stove) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,user,year,month,fan,tubelight,television,refrigerator,washing_machine,microwave_ovan,water_purifier,ac,water_heater,motor_pump,air_cooler,computer,electric_stove)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "Registered Success")
            result="sucess"

            

            mycursor.execute("SELECT * FROM eb_data where uname=%s",(user,))
            result = mycursor.fetchall()
            fn=user+".csv"
            with open('dataset/'+fn,'w') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(col[0] for col in mycursor.description)
                for row in result:
                    writer.writerow(row)

            with open('dataset/'+fn) as input, open('dataset/'+fn, 'w', newline='') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(col[0] for col in mycursor.description)
                for row in result:
                    if row or any(row) or any(field.strip() for field in row):
                        writer.writerow(row)
                        
            return redirect(url_for('view_data',act='yes')) 


    mycursor.execute("SELECT * FROM eb_data ")
    data2 = mycursor.fetchall()
    
   
        
    return render_template('view_data.html',cdata=cdata,data2=data2,act=act,mess=mess)

@app.route('/view_data1', methods=['GET', 'POST'])
def view_data1():
    msg=""
    cnt=0
    uname=""
    act=request.args.get("act")
    mess=request.args.get("mess")
    user=""
    if 'username' in session:
        uname = session['username']
    

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register")
    cdata = mycursor.fetchall()
    
    if request.method=='POST':
        user = request.form['user']

        filename=user+".csv"
        
        cdata = pd.read_csv("dataset/"+filename)

        mycursor.execute("delete FROM eb_data where uname=%s",(user,))
        mydb.commit()
        for ss in cdata.values:
        
            mycursor.execute("SELECT max(id)+1 FROM eb_data")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            
            
            sql = "INSERT INTO eb_data(id,uname,year,month,fan,tubelight,television,refrigerator,washing_machine,microwave_ovan,water_purifier,ac,water_heater,motor_pump,air_cooler,computer,electric_stove) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,user,ss[2],ss[3],ss[4],ss[5],ss[6],ss[7],ss[8],ss[9],ss[10],ss[11],ss[12],ss[13],ss[14],ss[15],ss[16])
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "Registered Success")
            result="sucess"


        return redirect(url_for('check',act='1')) 


    mycursor.execute("SELECT * FROM eb_data ")
    data2 = mycursor.fetchall()
    
   
        
    return render_template('view_data1.html',cdata=cdata,data2=data2,act=act,mess=mess)


@app.route('/check', methods=['GET', 'POST'])
def check():
    act=request.args.get("act")
    mess=request.args.get("mess")
    data2=[]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM eb_register")
    cdata = mycursor.fetchall()
    
    if request.method=='POST':
        user = request.form['user']
        f3=open("user.txt","w")
        f3.write(user)
        f3.close()
        act="yes"
        mycursor.execute("SELECT * FROM eb_data where uname=%s",(user, ))
        data2 = mycursor.fetchall()

 
        mycursor.execute("SELECT count(*) FROM eb_data where uname=%s",(user, ))
        du = mycursor.fetchone()[0]
        print(du)
        if du>=36:
            mess="1"
            mycursor.execute("update eb_register set train_st=1 where uname=%s",(user,))
            mydb.commit()
            
        else:
            mess="2"
       

    return render_template('check.html',act=act,mess=mess,cdata=cdata,data2=data2)


    

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75
    
    if request.method=='POST':
        return redirect(url_for('classify'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

##Random Forest
###############################################################################################
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		'''for row in csv_reader:
			if not row:
				continue
			dataset.append(row)'''
	return dataset
 
# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
 
# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup
 
# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 
# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
	return scores
 
# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
 
# Calculate the Gini index for a split dataset
def gini_index(groups, classes):
	# count all samples at split point
	n_instances = float(sum([len(group) for group in groups]))
	# sum weighted Gini index for each group
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		# score the group based on the score for each class
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / n_instances)
	return gini
 
# Select the best split point for a dataset
def get_split(dataset, n_features):
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	features = list()
	while len(features) < n_features:
		index = randrange(len(dataset[0])-1)
		if index not in features:
			features.append(index)
	for index in features:
		for row in dataset:
			groups = test_split(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}
 
# Create a terminal node value
def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return max(set(outcomes), key=outcomes.count)
 
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, n_features, depth):
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return
	# check for max depth
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	# process left child
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left, n_features)
		split(node['left'], max_depth, min_size, n_features, depth+1)
	# process right child
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right, n_features)
		split(node['right'], max_depth, min_size, n_features, depth+1)
 
# Build a decision tree
def build_tree(train, max_depth, min_size, n_features):
	root = get_split(train, n_features)
	split(root, max_depth, min_size, n_features, 1)
	return root
 
# Make a prediction with a decision tree
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']
 
# Create a random subsample from the dataset with replacement
def subsample(dataset, ratio):
	sample = list()
	n_sample = round(len(dataset) * ratio)
	while len(sample) < n_sample:
		index = randrange(len(dataset))
		sample.append(dataset[index])
	return sample
 
# Make a prediction with a list of bagged trees
def bagging_predict(trees, row):
	predictions = [predict(tree, row) for tree in trees]
	return max(set(predictions), key=predictions.count)
 
# Random Forest Algorithm
def random_forest(train, test, max_depth, min_size, sample_size, n_trees, n_features):
    trees = list()
    for i in range(n_trees):
            sample = subsample(train, sample_size)
            tree = build_tree(sample, max_depth, min_size, n_features)
            trees.append(tree)
    predictions = [bagging_predict(trees, row) for row in test]
    #return(predictions)

    # Test the random forest algorithm
    
    # load and prepare data
    filename = 'heart_processed.csv'
    dataset = '' #load_csv(filename)
    # convert string attributes to integers
    #for i in range(0, len(dataset[0])-1):
    #	str_column_to_float(dataset, i)
    # convert class column to integers
    #str_column_to_int(dataset, len(dataset[0])-1)
    # evaluate algorithm
    n_folds = 5
    max_depth = 10
    min_size = 1
    sample_size = 1.0
    #n_features = int(sqrt(len(dataset[0])-1))

##############################################################################################


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    cnt=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    data4=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    ayr=[]
    n=0
    a=""
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        
        
        if a==ss[0]:
            
            if n==0:
                ayr.append(a)
                    
            n+=1
        else:
            
            a=ss[0]
            n=0
            
        
        i+=1
    #print(ayr)
    cnt=len(ayr)
    j=0
    k=0
    
    aa1=[]
    data4=[]
    
        
    while j<cnt:
        a1=0
        a2=0
        a3=0
        a4=0
        a5=0
        a6=0
        a7=0
        a8=0
        a9=0
        a10=0
        a11=0
        a12=0
        a13=0
        for tt in data1.values:
            c1=tt[0]
            c2=tt[1]
            if ayr[j]==tt[0]:
                a1+=tt[2]
                a2+=tt[3]
                a3+=tt[4]
                a4+=tt[5]
                a5+=tt[6]
                a6+=tt[7]
                a7+=tt[8]
                a8+=tt[9]
                a9+=tt[10]
                a10+=tt[11]
                a11+=tt[12]
                a12+=tt[13]
                a13+=tt[14]
                aa1=[c1,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]
        data4.append(aa1)
                
        j+=1
        
    #print(data4)
    bb=''
    res=''
    data6=[]
    k=1
    ha = ['','Fan','Tubelight','Television','Refrigerator','Washing Mchine','Microwave Oven','Water Purifier','AC','Water Heater','Motor Pump','Air Cooler','Computer','Electric Steve']
    
    while k<=13:
        h1=data4[0][k]
        h2=data4[1][k]
        h3=data4[2][k]
        if h1>h2 and h1>h3:
            bb=str(ayr[0])
            df1=h1-h2
            df2=h1-h3
        elif h2>h3:
            bb=str(ayr[1])
            df1=h2-h1
            df2=h2-h3
        else:
            bb=str(ayr[2])
            df1=h3-h1
            df2=h3-h2

        if df1>=100 or df2>=100:
            res=ha[k]+" - "+bb
            data6.append(res)
        k+=1
        
    print(data6)  
    #print(data4[0][1])
    #print(data4[1][1])
    #print(data4[2][1])
    
    return render_template('classify.html',data4=data4,data6=data6)

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    msg=""
    cnt=0
    filename = 'upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    data4=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    ayr=[]
    n=0
    a=""
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        
        
        if a==ss[0]:
            
            if n==0:
                ayr.append(a)
                    
            n+=1
        else:
            
            a=ss[0]
            n=0
            
        
        i+=1
    #print(ayr)
    cnt=len(ayr)
    j=0
    k=0
    
    aa1=[]
    aa2=[]
    data4=[]
    data5=[]
        
    while j<cnt:
        a1=0
        a2=0
        a3=0
        a4=0
        a5=0
        a6=0
        a7=0
        a8=0
        a9=0
        a10=0
        a11=0
        a12=0
        a13=0
        for tt in data1.values:
            c1=tt[0]
            c2=tt[1]
            if ayr[j]==tt[0]:
                a1+=tt[2]
                a2+=tt[3]
                a3+=tt[4]
                a4+=tt[5]
                a5+=tt[6]
                a6+=tt[7]
                a7+=tt[8]
                a8+=tt[9]
                a9+=tt[10]
                a10+=tt[11]
                a11+=tt[12]
                a12+=tt[13]
                a13+=tt[14]
                aa1=[c1,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]
                aa2=[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]
        data4.append(aa1)
        data5.append(aa2)        
        j+=1
    
    #print(data4)
    # line 1 points
    x1 = ['Fan','Tubelight','Television','Refrigerator','Washing Mchine','Microwave Oven','Water Purifier','AC','Water Heater','Motor Pump','Air Cooler','Computer','Electric Steve']
    y1 = data5[0]
    # plotting the line 1 points 
    plt.plot(x1, y1, color='green', label = "2019")
      
    # line 2 points
    x2 = [1,2,3]
    y2 = data5[1]
    # plotting the line 2 points 
    plt.plot(x1, y2, color='blue', label = "2020")
      
    # line 3 points
    x3 = [1,2,3]
    y3 = data5[2]
    # plotting the line 2 points 
    plt.plot(x1, y3, color='red', label = "2021")
    

    # naming the x axis
    plt.xlabel('Home Appliances')
    # naming the y axis
    plt.ylabel('Energy Consumption')
    # giving a title to my graph
    plt.title('Yearwise Analysis')
      
    # show a legend on the plot
    plt.legend()
      
    # function to show the plot
    plt.show()
    return render_template('chart.html',data4=data4)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
