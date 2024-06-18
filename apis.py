import mysql.connector
import os
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()

#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')
print(mysql_password)

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = mysql_password,
    database = "project"
)

cursor = mydb.cursor()

@app.get("/rejectAds")
async def rejected(advertiseId:int, adminId:int):
    cursor.excute("update advertise set status='rejected', adApprover_id=adminId where ad_id=advertiseId")
    cursor.commit()

