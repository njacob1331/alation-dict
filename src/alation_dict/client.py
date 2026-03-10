from enum import Enum
import json
from collections.abc import Iterator
from typing import Any
import requests
from urllib.parse import urljoin

import warnings

warnings.filterwarnings("ignore")

from .record import Record

class Endpoint(Enum):
    COLUMN = 0

class Client:
    """
    API client for Alation endpoints.

    Auth
    ----
    Client requires authentication via API or Refresh token
    Authentication info: https://developer.alation.com/dev/docs/authentication-into-alation-apis
    """

    def __init__(self, auth_token: str):
        self.base_url: str = "https://alation.medcity.net/"
        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "token": auth_token
        })

    def _get(self, url: str, params: dict[str, Any] | None):
        """
        Internal method for handling GET request boilerplate.
        """
        response = self.session.get(
            url=url,
            params=params,
            verify=False
        )

        response.raise_for_status()

        next_page = response.headers.get("X-Next-Page")
        next_page_url = urljoin(self.base_url, next_page) if next_page else None

        return response, next_page_url

    def _get_integration_v2_column(self):
        """
        GET request for the integration/v2/column/ endpoint
        """

        url = urljoin(self.base_url, "/integration/v2/column/")
        params = {
            "fields": "id,name,title,description,url,ds_id,table_name,custom_fields",
            "ds_id": 15,
            "custom_fields": json.dumps(
                [{"field_id": 10049, "value": "Approved"}]
            )
        }

        while url:
            response, url = self._get(url, params)
            params = None

            for record in response.json():
                yield Record(**record)

    def get(self, endpoint: Endpoint) -> Iterator[Record]:
        """
        GET request to endpoint
        """

        # this pattern makes it easy to support more endpoints in the future
        match endpoint:
            case Endpoint.COLUMN:
                yield from self._get_integration_v2_column()

    def _patch(self, url: str, body: dict[str, Any]):
        """
        Internal method for handling PATCH request boilerplate.
        """

        response = self.session.patch(
            url=url,
            json=[body],
            verify=False
        )

        response.raise_for_status()

    def _patch_integration_v2_column(self, body: dict[str, Any]):
        """
        PATCH request for the integration/v2/column/ endpoint
        """

        url = urljoin(self.base_url, "/integration/v2/document/?ds_id=15")
        self._patch(url, body)

    def patch(self, endpoint: Endpoint, body: dict[str, Any]):
        """
        PATCH request to endpoint
        """
        match endpoint:
            case Endpoint.COLUMN:
                self._patch_integration_v2_column(body)
