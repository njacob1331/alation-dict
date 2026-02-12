import json
from collections.abc import Iterator
from pydantic import BaseModel, ConfigDict
import requests
from urllib.parse import urljoin

import warnings
warnings.filterwarnings("ignore")

from .record import Record

class CustomField(BaseModel):
    field_id: int
    value: str

class Config(BaseModel):
    fields: str
    custom_fields: list[CustomField]

    model_config = ConfigDict(
        extra="allow",
        frozen=True
    )

    @classmethod
    def load_or_default(cls, path: str | None) -> Config:
        if path is None:
            return cls.default()
        try:
            with open(path, "r") as f:
                raw = json.load(f)
            return cls(**raw)
        except Exception:
            return cls.default()

    @classmethod
    def default(cls) -> Config:
        return cls(
            fields="id,name,title,description,url",
            custom_fields=[
                CustomField(
                    field_id=10049,
                    value="Approved"
                )
            ]
        )

    def serialize(self) -> dict[str, str]:
        return {
            "fields": self.fields,
            "custom_fields": json.dumps(
                [cf.model_dump() for cf in self.custom_fields]
            )
        }

class Client:
    """
    API client for the Alation 'column' endpoint: https://alation.medcity.net/integration/v2/column/

    Auth
    ----
    Client requires authentication via API or Refresh token
    Authentication info: https://developer.alation.com/dev/docs/authentication-into-alation-apis

    Request params
    --------------
    Request params are set via a config file (json). If a file is not provided or
    the file cannot be read, default params are set.

    """

    def __init__(self, auth_token: str, config_path: str | None = None):
        config = Config.load_or_default(config_path)

        self.params: dict[str, str] = config.serialize()
        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "token": auth_token
        })

        self.base_url: str = "https://alation.medcity.net/integration/v2/column/"
        self.next_response_url: str | None = self.base_url

    def _get(self):
        """
        Internal Client method for performing GET request to Alation API
        """
        response = self.session.get(
            url=self.next_response_url or self.base_url,
            params=self.params if self.next_response_url == self.base_url else None,
            verify=False
        )

        response.raise_for_status()

        next_page = response.headers.get("X-Next-Page")
        self.next_response_url = (
            urljoin(self.base_url, next_page) if next_page else None
        )

        for record in response.json():
            yield Record(**record)

    def api_response(self) -> Iterator[Record]:
        """
        Iterates through paginated API responses and yields each record.
        """
        while self.next_response_url:
            yield from self._get()
