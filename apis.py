import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
#...import fastapi packages.......
from fastapi import FastAPI,Query,Path, Body, Header 
from pydantic import BaseModel, Field
from typing import Optional ,Union,Tuple ,Annotated
#...import fastapi packages.......
from models import Advertise





#import pass from env variable
load_dotenv()
mysql_password = os.getenv('mysql_password')

app = FastAPI() 

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", #enter your mysql username
    password = mysql_password ,
    database = "Project"
)

cursor = mydb.cursor() # create an instance of cursor class to execute mysql commands





#amiralis apis.....................................................................

@app.post("/{publisher_id}/advertise")
async def student_data(a1: Advertise,publisher_id: int):
   return a1



#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

