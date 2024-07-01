from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, List

class Advertise(BaseModel):
    price: float = Field(..., title="Price associated with the advertisement")
    description: str = Field(..., title="Description of the advertisement", max_length=200)
    title: str = Field(..., title="Title of the advertisement", max_length=100)
    phone_number: str = Field(..., title="Contact phone number for the advertisement", max_length=11)
    city: str = Field(..., title="name of city related to the advertisement")
    type_name: str = Field(..., title="Type of the advertisement")


class Report(BaseModel):
    note: str = Field(..., title="note of report")
    type_name: str = Field(..., title="category of report")

# You may need to adjust types and constraints as per your actual database schema.


class advertiseOut(BaseModel):
    ad_id:int
    published_at: datetime
    price: float
    title: str
    desc: Optional[str]
    phone_number: str
    city:str
    publisher_id : int
    cat_id: int




class Shop(BaseModel):
    founderId: int
    name: str
    address: str
    city: str

class userIn(BaseModel):
    phone_number:str
    city:str
    email:str
    fname:str
    lname:str
    gender:int    

