from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field, validator

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



class UserProfile(BaseModel):
    user_id: int
    age: Optional[int] = Field(None, title="Age of the user")
    phone_number: str = Field(..., title="Phone number of the user", max_length=11)
    city: str = Field(..., title="City of the user", max_length=15)
    email: str = Field(..., title="Email of the user", max_length=40)
    registration_date: str = Field(..., title="Registration date of the user")
    first_name: str = Field(..., title="First name of the user", max_length=25)
    last_name: str = Field(..., title="Last name of the user", max_length=25)
    profile_image_url: str | None # Field for the profile image URL
    type: int = Field(..., title="Type of the user", ge=1, le=2)
    salary: float = Field(..., title="Salary of the user")
    gender: int = Field(..., title="Gender of the user", ge=1, le=2)
    active: bool = Field(..., title="Active status of the user")

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=25)
    last_name: Optional[str] = Field(None, max_length=25)
    city: Optional[str] = Field(None, max_length=15)
    age: Optional[int] = Field(None, gt=10, description="Age must be greater than 10")
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=11, pattern="^\d{11}$")

    @validator('phone_number')
    def phone_number_must_be_valid(cls, v):
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        return v
    
class AdReview(BaseModel):
    status: str = Field(..., title="Status of the advertisement ('accepted' or 'rejected')")