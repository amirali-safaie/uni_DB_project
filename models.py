from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, List


class AdReview(BaseModel):
    status: str = Field(..., title="Status of the advertisement ('accepted' or 'rejected')")
