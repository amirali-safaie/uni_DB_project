from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Advertisement(BaseModel):
    expiration_date: Optional[datetime] = Field(None, title="Expiration date of the advertisement")
    price: Optional[float] = Field(None, title="Price associated with the advertisement")
    published_at: Optional[datetime] = Field(None, title="Publication date of the advertisement")
    description: Optional[str] = Field(None, title="Description of the advertisement", max_length=200)
    title: str = Field(..., title="Title of the advertisement", max_length=100)
    phone_number: Optional[str] = Field(None, title="Contact phone number for the advertisement", max_length=11)
    view_number: int = Field(0, title="Number of views for the advertisement")
    city_id: Optional[int] = Field(None, title="ID of city related to the advertisement")
    publisher_id: Optional[int] = Field(None, title="ID of publisher who posted the advertisement")
    status: str = Field(..., title="Status of approval for posting", enum=["rejected","pending","accepted"])
    # Assuming 'deleted' is a boolean field indicating if the ad is deleted or not
    deleted: bool = Field(False, title="Is the advertisement deleted?")
    # Assuming 'type' is an integer field in your table
    type: int = Field(..., title="Type of the advertisement")
    adApprover_id: Optional[int] = Field(None, title="ID of the approver for the advertisement")

# You may need to adjust types and constraints as per your actual database schema.
