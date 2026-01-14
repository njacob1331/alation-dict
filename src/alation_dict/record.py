from typing import ClassVar
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, field_validator

class Record(BaseModel):
    """
    Type respresenting both the Alation API response object
    and corresponding dictionary entry.
    """
    base_url: ClassVar[str] = "https://alation.medcity.net"
    model_config = ConfigDict(
        extra="allow",
        frozen=True
    )

    id: int
    name: str
    title: str
    description: str
    url: str

    @field_validator("description")
    def format_description(cls, v: str):
        return BeautifulSoup(v, "html.parser").get_text(strip=True)

    @field_validator("url")
    def format_url(cls, v: str):
        return urljoin(cls.base_url, v)
