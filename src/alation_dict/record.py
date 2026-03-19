from typing import Any, ClassVar, Self
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

CUSTOM_FIELD_ID_MAP = {
    10030: "phi",
    10031: "pii",
    10045: "page_status",
}

class Record(BaseModel):
    """
    Type respresenting both the Alation API response object
    and corresponding dictionary entry for columns.
    """
    base_url: ClassVar[str] = "https://alation.medcity.net"
    model_config = ConfigDict(
        extra="ignore",
        frozen=True
    )

    id: int
    name: str
    title: str
    description: str
    url: str
    table_name: str
    page_status: str | None
    phi: str | None
    pii: str | None

    @model_validator(mode="before")
    def destructure_custom_fields(cls, data: Any):
        """
        Maps the array of custom fields received from Alation to Record fields
        """
        for attr in CUSTOM_FIELD_ID_MAP.values():
            data.setdefault(attr, None)

        for field in data["custom_fields"]:
            attr = CUSTOM_FIELD_ID_MAP.get(field["field_id"])
            if attr:
                data[attr] = field["value"]

        return data

    @field_validator("description")
    def format_description(cls, v: str):
        # Alation stores descriptions as raw html
        return BeautifulSoup(v, "html.parser").get_text(strip=True)

    @field_validator("url")
    def format_url(cls, v: str):
        # Builds the full url for each column record
        return urljoin(cls.base_url, v)

    @classmethod
    def patch(cls, record: Self, to: dict[str, Any]):
        """
        Patches a record with the values provided.
        """
        return record.model_copy(update=to)

    @classmethod
    def patch_batch(cls, records: list[Self], to: dict[str, Any]):
        """
        Patches multiple records with the values provided.
        """
        return [cls.patch(record, to) for record in records]
