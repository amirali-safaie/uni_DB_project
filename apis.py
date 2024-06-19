import mysql.connector
import os
from dotenv import load_dotenv
#...import fastapi packages.......
from fastapi import FastAPI,Query,Path, Body, Header, HTTPException 
from pydantic import BaseModel, Field
from typing import Optional ,Union,Tuple ,Annotated
from models import Shop



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
     


#Hossein apis........................................................................



#amiralis apis.....................................................................

#amiralis apis.....................................................................

# cursor.execute("drop database project") #example of how run sql command on file 

