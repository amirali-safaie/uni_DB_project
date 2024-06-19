from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Advertisement(BaseModel):
    price: Optional[float] = Field(None, title="Price associated with the advertisement")
    description: Optional[str] = Field(None, title="Description of the advertisement", max_length=200)
    title: str = Field(..., title="Title of the advertisement", max_length=100)
    phone_number: Optional[str] = Field(None, title="Contact phone number for the advertisement", max_length=11)
    city_id: Optional[int] = Field(None, title="ID of city related to the advertisement")

# You may need to adjust types and constraints as per your actual database schema.


