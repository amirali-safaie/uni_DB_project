import io
import json
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Query, Path, Body, Header, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, Union, Tuple
from models import AdReview, UserProfile, UserProfileUpdate

# Import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")

# Creating connection object
mydb = mysql.connector.connect(
    host="localhost",
    user="root",  # enter your MySQL username
    password=mysql_password,
    database="myproject"
)

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
    
    return {"message": f"Advertise ID {advertise_id} has been updated to status '{review.status}'"}

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

    return {"message": "Profile image uploaded successfully"}

@app.get("/user/{user_id}/profile-image")
async def get_profile_image(user_id: int):
    cursor.execute("""
        SELECT profile
        FROM user
        WHERE user_id = %s
    """, (user_id,))
    
    result = cursor.fetchone()
    if not result or not result[0]:
        raise HTTPException(status_code=404, detail="Profile image not found")
    
    return StreamingResponse(io.BytesIO(result[0]), media_type="image/jpeg")
