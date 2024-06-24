import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
#...import fastapi packages.......
from fastapi import FastAPI, Query, Path, Body, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Union, Tuple, Annotated, List
#...import fastapi packages.......
from models import   AdReview

# Import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI() 

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",  # enter your MySQL username
    password = mysql_password,
    database = "myproject"
)

cursor = mydb.cursor()  # create an instance of cursor class to execute MySQL commands

# API 4
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