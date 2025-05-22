from pydantic import BaseModel
from typing import List

class AttendeesRequest(BaseModel):
    emails: List[str]
