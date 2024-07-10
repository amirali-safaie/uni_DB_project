import io
import json
import mysql.connector
import os
import smtplib, ssl, random, datetime
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Query, Path, Body, Header, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse,HTMLResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, Union, Tuple
from models import AdReview, UserProfile, UserProfileUpdate,userIn
import redis 
# Import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')
r = redis.Redis("localhost")
app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", #enter your mysql username
    password = mysql_password ,
    database = "Project"
)

cursor = mydb.cursor() # create an instance of cursor class to execute mysql commands



#Hossein apis.......................................................................
@app.get("/advertises")  #number 14
async def list_of_advertises(request: Request):
    cursor.execute(f"select ad_id,price,title from advertise where deleted = {0} ")
    responses = cursor.fetchall()
    return templates.TemplateResponse("show_advertise_list.html", {"request": request,"responses":responses})



#number 14
@app.post("/rejectAd/{advertiseId}")
async def reject(advertiseId:int,request:Request):
    cursor.execute(f"update advertise set deleted={1} where ad_id={advertiseId}")
    mydb.commit()
    cursor.execute(f"select ad_id,price,title from advertise where deleted = {0} ")
    responses = cursor.fetchall()
    return templates.TemplateResponse("show_advertise_list.html", {"request": request,"responses":responses})


@app.get("/fill-shop/{founderId}") #number 14
async def fill_shop(request: Request,founderId:int):
    return templates.TemplateResponse("fill_add_shop.html", {"request": request,'founderId':founderId})





@app.post("/addShop/{founderId}") #number 11
async def addShop(founderId:int,request:Request,city: str = Form(...), address: str = Form(...),name :str= Form(...)):
    isFound = False
    cursor.execute("select cityName from city")
    records = cursor.fetchall()
    for x in records:
        if(city == x[0]):  
            isFound = True
            break
    if(not isFound): # incorrect city in input
        raise HTTPException(status_code=400, detail="the city is incorrect") 
    
    cursor.execute("select founder_id from shop")
    records = cursor.fetchall()
    for x in records:
         if(x[0] == founderId):   #find the user that found the shop
            raise HTTPException(status_code=400, detail="you have already shop")    

    cursor.execute("""
    INSERT INTO shop (founder_id, name, address, city) 
    VALUES (%s, %s, %s, %s)
    """, (founderId, name, address, city))

    mydb.commit()
    return templates.TemplateResponse("fill_add_shop.html", {"request": request,'founderId':founderId})
     

@app.get("/getMostReceantlyAds")  
async def get_most(request:Request):
    cursor.execute(f"select ad_id,title,price from advertise where status='accepted' order by published_at desc limit 5")
    records = cursor.fetchall()
    print(records)
    return templates.TemplateResponse("show_most_advertise.html", {"request": request,'responses':records})


@app.get("/filterAdvertise")  #number 8
async def filter(typee:str, low_price:int|None=0, high_price:int|None=200000000000):
    cursor.execute(f"select * from advertise where price > {low_price} and price < {high_price} and  type = (select cat_id from category where name='{typee}');")
    records = cursor.fetchall()
    listOfAdvertises = []
    for x in records:
        ad = advertiseOut(ad_id=x[0], published_at=x[2], price=x[3], title=x[4], desc=x[5], phone_number=x[7], city=x[8], publisher_id=x[9], cat_id=x[12])
        listOfAdvertises.append(ad)

    return {"list of advertises" : listOfAdvertises}    


@app.get("/sendEmail")
async def send(email:str):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "hosseinabedinipoco@gmail.com"  # Enter your address
    receiver_email = email  # Enter receiver address
    password = "ahwkbhvcjkjlscbd"
    num = random.randint(1000, 9999)
    message = str(num)
    r.setex(email, message, 120)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


@app.get("/login")
async def login(password:int, email:str):
    cursor.execute(f"select * from user where email='{email}'")
    record = cursor.fetchall()
    if(len(record) == 0):
        raise HTTPException(status_code=400, detail="there is not this email")
    if(password != int(r.get(email))):
        raise HTTPException(status_code=400, detail="incorect password")   
    return {"message" : "succesful"}

@app.post("/signup")
async def signup(user:userIn, password:int):
    cursor.execute(f"select * from user where email='{user.email}'")
    record = cursor.fetchall()
    if(len(record) != 0):
        raise HTTPException(status_code=400, detail="this email is already exists")
    cursor.execute(f"select * from user where phone_number='{user.phone_number}'")
    record = cursor.fetchall()
    if(len(record) != 0):
        raise HTTPException(status_code=400, detail="this phone number is already exists")
    if(password != int(r.get(user.email))):
        raise HTTPException(status_code=400, detail="incorect password")
    
    date = datetime.now()
    cursor.execute(f"INSERT INTO user (phone_number, city, email, registration_date, first_name, last_name, type, salary, gender, active) VALUES ('{user.phone_number}', '{user.city}', '{user.email}', '{date}', '{user.fname}', '{user.lname}', 1, 0, {user.gender}, TRUE)")
    mydb.commit()

    return {"message" : "the user added succesfully"}

#Hossein apis........................................................................



#Hossein apis........................................................................



#amiralis apis.....................................................................

@app.get("/fill-advertise/{publisherId}", response_class=HTMLResponse)
async def fill_advertise(publisherId:int,request: Request):
   return templates.TemplateResponse("publish_advertise.html", {"request": request,"publisherId":publisherId})



@app.post("/{publisherId}/advertise")
async def publish_advertise(publisherId:int,price: int = Form(...), title: str = Form(...),description: str = Form(...),city: str = Form(...),phone_number: str = Form(...),category: str = Form(...)):
    today = datetime.now()
    two_weeks_later = today + timedelta(weeks=2)
    expiration_date = two_weeks_later.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(f"""
    INSERT INTO advertise (expiration_date, published_at, price, title, 
    description, status, phone_number, city, publisher_id,type , deleted)
    VALUES ('{expiration_date}', '{today}', {price}, '{title}', '{description}', 'pending', '{phone_number}',
    '{city}',{publisherId},(SELECT cat_id FROM category WHERE name = '{category}'), {0});""")

cursor = mydb.cursor()  # create an instance of cursor class to execute MySQL commands

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile")
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/review")
async def review_page(request: Request):
    return templates.TemplateResponse("review.html", {"request": request})

@app.get("/reports")
async def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})

@app.get("/user_login")
async def user_login_page(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})

@app.get("/user_actions/{user_id}")
async def user_actions_page(request: Request, user_id: int):
    return templates.TemplateResponse("user_actions.html", {"request": request, "user_id": user_id})
@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/review")
async def review_page(request: Request):
    return templates.TemplateResponse("review.html", {"request": request})

@app.get("/reports")
async def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})


@app.patch("/support/advertise/{advertise_id}/status")
async def review_advertise(advertise_id: int, review: AdReview):
    allowed_statuses = {"rejected", "accepted"}
    
    if review.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status value. Allowed values are 'rejected', 'accepted'")
    
    cursor.execute("""
        UPDATE advertise 
        SET status = %s
        WHERE ad_id = %s
    """, (review.status, advertise_id))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Advertise not found")
    
    mydb.commit()


@app.get("/advertise/{advertiseId}",response_class=HTMLResponse)
async def visit_advertise(advertiseId:int,request: Request):

    cursor.execute(f"""
    select published_at,price,title,phone_number,city,
    (select c.name from category as c where c.cat_id = a.type)
    from advertise as a 
    where a.ad_id = {advertiseId} and a.status = 'accepted' """)

    result = cursor.fetchone()
    print(result)
    cursor.execute(f"""
    update advertise 
    set view = view + 1
    where advertise.ad_id = {advertiseId}
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
    

@app.get("/support/reports")
async def get_ad_reports():
    cursor.execute("""
        SELECT r.report_id, r.writer_id, r.Moderator_id, r.advertise_id, r.note, r.status, rc.name AS type_name
        FROM report r
        INNER JOIN report_category rc ON rc.cat_id = r.type
        ORDER BY r.report_id DESC
    """)
    
    reports = cursor.fetchall()
    
    response = []
    for report in reports:
        response.append({
            "report_id": report[0],
            "writer_id": report[1],
            "moderator_id": report[2],
            "advertise_id": report[3],
            "note": report[4],
            "status": report[5],
            "type_name": report[6]
        })
    
    return response


@app.get("/{userId}/advertises")
async def published_advertise_user(userId: int,request: Request):


    cursor.execute(f"""
    select title,phone_number,city,status,view
    from advertise 
    where advertise.publisher_id = {userId}""")

    responses = cursor.fetchall()
    print(responses)

    return templates.TemplateResponse("advertises_of_user.html", {"request": request, "responses":responses})




@app.get("/users")
async def list_of_users(request: Request):


    cursor.execute(f"""
    select user_id,first_name,last_name
    from user
    where type = 1 and active = 1;
    """)

    responses = cursor.fetchall()

    return templates.TemplateResponse("list_of_users.html", {"request":request,"responses":responses})




@app.post("/deactivate/{userId}")
async def deactivate_user(userId: int):

    cursor.execute(f"""
    update user
    set active = 0
    where user_id = {userId}""")

    mydb.commit()



@app.get("/user/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: int):
    cursor.execute("""
        SELECT user_id, age, phone_number, city, email, registration_date, first_name, last_name, profile, type, salary, gender, active
        FROM user
        WHERE user_id = %s
    """, (user_id,))
    
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    image_url = None
    if result[8]:  # Assuming the profile image is stored in the 9th column
        image_url = f"http://localhost:8000/user/{user_id}/profile-image"
    
    user_profile = UserProfile(
        user_id=result[0],
        age=result[1],
        phone_number=result[2],
        city=result[3],
        email=result[4],
        registration_date=result[5].strftime('%Y-%m-%d %H:%M:%S'),
        first_name=result[6],
        last_name=result[7],
        profile_image_url=image_url,
        type=result[9],
        salary=result[10],
        gender=result[11],
        active=result[12]
    )
    return user_profile


@app.patch("/user/{user_id}/profileChanges")
async def update_user_profile(user_id: int, profile_data: UserProfileUpdate = Body(...)):
    # Check if user exists
    cursor.execute("SELECT 1 FROM user WHERE user_id = %s", (user_id,))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated = False

    # Update each field if it's provided
    for field, value in profile_data.dict(exclude_unset=True).items():
        if value is not None:
            cursor.execute(f"""
                UPDATE user
                SET {field} = %s
                WHERE user_id = %s
            """, (value, user_id))
            if cursor.rowcount > 0:
                updated = True
    if updated:
        mydb.commit()
        return {"message": f"User ID {user_id} profile has been updated"}
    else:
        return {"message": "No updates made to the user profile"}

@app.post("/user/{user_id}/upload-profile-image")
async def upload_profile_image(user_id: int, file: UploadFile = File(...)):
    file_contents = await file.read()
    
    cursor.execute("""
        UPDATE user
        SET profile = %s
        WHERE user_id = %s
    """, (file_contents, user_id))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    mydb.commit()
     
    return "deactivated"




@app.get("/{userId}/fill-report/{advertiseId}")
async def fill_report(user_id: int,advertise_id:int,request: Request):

   return templates.TemplateResponse("fill_report.html", {"request": request,"advertise_id":advertise_id,"user_id":user_id} )




@app.post("/{user_id}/report/advertise/{advertise_id}")
async def report_advertise(user_id: int,advertise_id:int,note: str = Form(...), type_name: str = Form(...)):


    cursor.execute(f"""
    INSERT INTO report (note, status, writer_id, advertise_id, type) VALUES 
    ('{note}', 'pending', {user_id}, {advertise_id}, 
    (SELECT cat_id FROM report_category WHERE name = '{type_name}'));
    """)

    mydb.commit()



#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

