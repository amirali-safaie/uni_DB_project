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

# You may need to adjust types and constraints as per your actual database schema.


