from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, field_validator

class Record(BaseModel):
    """
    Type respresenting both the Alation API response object
    and corresponding dictionary entry.
    """
    model_config = ConfigDict(extra="allow")

    id: int
    name: str
    title: str
    description: str

    @field_validator("description")
    def format_description(cls, v: str):
        return BeautifulSoup(v, "html.parser").get_text(strip=True)
