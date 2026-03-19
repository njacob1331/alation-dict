from enum import Enum
import json
from collections.abc import Iterator
from typing import Any
import requests
from urllib.parse import urljoin

# this serves only to suppress requests warnings
# during dev. in prod, verify should be set = True
# and this can be removed
import warnings
warnings.filterwarnings("ignore")

from .record import Record

class Endpoint(Enum):
    """
    Endpoints supported by the API Client. Each variant
    carries default request params that are used if params are not
    set by the user.
    """
    # ref: https://developer.alation.com/dev/reference/getcolumns
    COLUMN = {
        "fields": "id,name,title,description,url,table_name,custom_fields",     # fields we want returned
        "ds_id": 15,                                                            # maps to HCA- BigQuery - HIN DEV
        "custom_fields": json.dumps(                                            # filters for Verification Status = "Approved"
            [{"field_id": 10049, "value": "Approved"}]
        )
    }

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
        GET request boilerplate
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

    def _get_integration_v2_column(self, params: dict[str, Any] | None = None):
        """
        GET request for the integration/v2/column/ endpoint
        """

        url = urljoin(self.base_url, "/integration/v2/column/")

        while url:
            response, url = self._get(url, params)
            params = None   # params are already present in 'next page' urls

            for record in response.json():
                yield Record(**record)

    def get(self, endpoint: Endpoint, params: dict[str, Any] | None = None) -> Iterator[Record]:
        """
        GET request to endpoint
        """
        # this pattern makes it easy to support more endpoints in the future (ex we want to
        # fetch data quality rules from Alation)
        match endpoint:
            case Endpoint.COLUMN:
                yield from self._get_integration_v2_column(params or endpoint.value)
            # case Endpoint.ANOTHER:
                # yield from self._get_another_endpoint(params or endpoint.value)
