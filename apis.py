import mysql.connector
import os
import smtplib, ssl, random, datetime
from dotenv import load_dotenv
from datetime import datetime, timedelta
#...import fastapi packages.......
from fastapi import FastAPI,Query,Path, Body,Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional ,Union,Tuple ,Annotated
#...import fastapi packages.......
from models import Advertise,Report,Shop, advertiseOut, userIn

#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI() 
templates = Jinja2Templates(directory="templates")

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", #enter your mysql username
    password = mysql_password ,
    database = "project"
)

cursor = mydb.cursor() # create an instance of cursor class to execute mysql commands



#Hossein apis.......................................................................
@app.get("/rejectAd")  #number 14
async def reject(advertiseId:int):
    cursor.execute(f"update advertise set deleted=TRUE where ad_id={advertiseId}")
    mydb.commit()
    return {"message": f"the advertise {advertiseId} deleted"}


@app.post("/addShop") #number 11
async def addShop(shop : Shop):
    isFound = False
    cursor.execute("select cityName from city")
    records = cursor.fetchall()
    for x in records:
        if(shop.city == x[0]):  
            isFound = True
            break
    if(not isFound): # incorrect city in input
        raise HTTPException(status_code=400, detail="the city is incorrect") 
    
    cursor.execute("select founder_id from shop")
    records = cursor.fetchall()
    for x in records:
         if(x[0] == shop.founderId):   #find the user that found the shop
            raise HTTPException(status_code=400, detail="you have already shop")    

    cursor.execute("""
    INSERT INTO shop (founder_id, name, address, city) 
    VALUES (%s, %s, %s, %s)
""", (shop.founderId, shop.name, shop.address, shop.city))

    mydb.commit()
    return {"message": "shop added succesfully"}
     

@app.get("/getMostReceantlyAds")   #number 5
async def get():
     cursor.execute("select * from advertise where deleted = FALSE   and status='accepted' order by published_at desc limit 5")
     records = cursor.fetchall()
     listOfAdvertis = []
     for x in records:
          ad = advertiseOut(ad_id=x[0], published_at=x[2], price=x[3], title=x[4], desc=x[5], phone_number=x[7], city=x[8], publisher_id=x[9], cat_id=x[12])
          listOfAdvertis.append(ad)
          
     return {"list of advertises" : listOfAdvertis}


@app.get("/filterAdvertise")  #number 8
async def filter(typee:str, low_price:int|None=0, high_price:int|None=200000000000):
    cursor.execute(f"select * from advertise where price > {low_price} and price < {high_price} and  type = (select cat_id from category where name='{typee}');")
    records = cursor.fetchall()
    listOfAdvertises = []
    for x in records:
        ad = advertiseOut(ad_id=x[0], published_at=x[2], price=x[3], title=x[4], desc=x[5], phone_number=x[7], city=x[8], publisher_id=x[9], cat_id=x[12])
        listOfAdvertises.append(ad)

    return {"list of advertises" : listOfAdvertises}    


passs = {}
@app.get("/sendEmail")
async def send(email:str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "hosseinabedinipoco@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "ahwkbhvcjkjlscbd"
    num = random.randint(1000, 9999)
    message = str(num)
    passs[email] = message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@app.get("/login")
async def login(password:str, email:str):
    cursor.execute(f"select * from user where email='{email}'")
    record = cursor.fetchall()
    if(len(record) == 0):
        raise HTTPException(status_code=400, detail="there is not this email")
    try:
        if(password != passs[email]):
            raise HTTPException(status_code=400, detail="incorect password")
    except:
        raise HTTPException(status_code=400, detail="email was not send")    
    passs.pop(email)
    return {"message" : "succesful"}

@app.post("/signup")
async def signup(user:userIn, password:str):
    cursor.execute(f"select * from user where email='{user.email}'")
    record = cursor.fetchall()
    if(len(record) != 0):
        raise HTTPException(status_code=400, detail="this email is already exists")
    cursor.execute(f"select * from user where phone_number='{user.phone_number}'")
    record = cursor.fetchall()
    if(len(record) != 0):
        raise HTTPException(status_code=400, detail="this phone number is already exists")
    try:
        if(password != passs[user.email]):
            raise HTTPException(status_code=400, detail="incorect password")
    except:
        raise HTTPException(status_code=400, detail="the email was not send")
    
    date = datetime.datetime.now()
    cursor.execute(f"INSERT INTO user (phone_number, city, email, registration_date, first_name, last_name, type, salary, gender, active) VALUES ('{user.phone_number}', '{user.city}', '{user.email}', '{date}', '{user.fname}', '{user.lname}', 1, 0, {user.gender}, TRUE)")
    mydb.commit()
    passs.pop(user.email)
    return {"message" : "the user added succesfully"}

#Hossein apis........................................................................



#amiralis apis.....................................................................

@app.post("/{publisher_id}/advertise")
async def publish_advertise(a1: Advertise,publisher_id: int):
    today = datetime.now()
    two_weeks_later = today + timedelta(weeks=2)
    expiration_date = two_weeks_later.strftime('%Y-%m-%d %H:%M:%S')


    cursor.execute(f"""
    INSERT INTO advertise (expiration_date, published_at, price, title, 
    description, status, phone_number, city, publisher_id,type , deleted)
    VALUES ('{expiration_date}', '{today}', {a1.price}, '{a1.title}', '{a1.description}', 'pending', '{a1.phone_number}',
    '{a1.city}',{publisher_id},(SELECT cat_id FROM category WHERE name = '{a1.type_name}'), FALSE);""")

    mydb.commit()

    return f'advertise with {a1.title} is registered'


@app.get("/advertise/{advertise_id}",response_class=HTMLResponse)
async def visit_advertise(advertise_id:int,request: Request):

    cursor.execute(f"""
    select published_at,price,title,phone_number,city,
    (select c.name from category as c where c.cat_id = a.type)
    from advertise as a 
    where a.ad_id = {advertise_id} and a.status = 'accepted' """)

    result = cursor.fetchone()
    print(result)
    cursor.execute(f"""
    update advertise 
    set view = view + 1
    where advertise.ad_id = {advertise_id}
    """)

    mydb.commit()


    response = {
        "title": result[2],
        "published_at": str(result[0]),
        "price": result[1],
        "category": result[5],
        "comminucate_way": result[3],
        "city": result[4],
    }

    return templates.TemplateResponse("advertise_detail.html", {"request": request, "response":response})


@app.get("/{user_id}/advertises")
async def published_advertise_user(user_id: int):


    cursor.execute(f"""
    select title,phone_number,city,status,view
    from advertise 
    where advertise.publisher_id = {user_id}""")

    result = cursor.fetchall()
    nl = '\n'
    return f'list of advertises: \n {result}'

@app.patch("/deactivate/{user_id}")
async def deactivate_user(user_id: int):


    cursor.execute(f"""
    update user
    set active = 0
    where user_id = {user_id}""")

    mydb.commit()

    return f'user with {user_id} deactivated'

@app.post("/{user_id}/advertise/{advertise_id}")
async def deactivate_user(user_id: int,advertise_id:int,r1:Report):


    cursor.execute(f"""
    INSERT INTO report (note, status, writer_id, advertise_id, type) VALUES 
    ('{r1.note}', 'pending', {user_id}, {advertise_id}, 
    (SELECT cat_id FROM report_category WHERE name = '{r1.type_name}'));
    """)

    mydb.commit()

    return f'advertise reported by {user_id}'


#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

