from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator

class Record(BaseModel):
    """
    Class which adds stronger typing for both the Alation API response object
    and corresponding dictionary entry.
    """
    id: int
    name: str
    title: str
    description: str

    @field_validator("description")
    def format_description(cls, v):
        return BeautifulSoup(v, "html.parser").get_text(strip=True)
