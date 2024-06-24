import mysql.connector
import os
import smtplib, ssl, random, datetime
from dotenv import load_dotenv
#...import fastapi packages.......
from fastapi import FastAPI,Query,Path, Body, Header, HTTPException 
from pydantic import BaseModel, Field
from typing import Optional ,Union,Tuple ,Annotated
from models import Shop, advertiseOut, userIn


#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI() 
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
    if(password != passs[email]):
        raise HTTPException(status_code=400, detail="incorect password")
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
    if(password != passs[user.email]):
        raise HTTPException(status_code=400, detail="incorect password")
    date = datetime.datetime.now()
    cursor.execute(f"INSERT INTO user (phone_number, city, email, registration_date, first_name, last_name, type, salary, gender, active) VALUES ('{user.phone_number}', '{user.city}', '{user.email}', '{date}', '{user.fname}', '{user.lname}', 1, 0, {user.gender}, TRUE)")
    mydb.commit()
    passs.pop(user.email)
    return {"message" : "the user added succesfully"}

#Hossein apis........................................................................



#amiralis apis.....................................................................

#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

