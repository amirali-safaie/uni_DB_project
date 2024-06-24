import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
#...import fastapi packages.......
from fastapi import FastAPI, Query, Path, Body, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Union, Tuple, Annotated, List
#...import fastapi packages.......
from models import Advertise, UserProfileUpdate, AdReport, AdReview

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

