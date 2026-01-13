import json
from collections.abc import Iterator
import requests
from urllib.parse import urljoin

from .record import Record

class Client:
    """
    API client for the Alation 'column' endpoint: https://alation.medcity.net/integration/v2/column/

    Auth
    ----
    Client requires authentication via API or Refresh token
    Authentication info: https://developer.alation.com/dev/docs/authentication-into-alation-apis

    Request params
    --------------
    Default parameters are set to filter for verification status = 'Approved'.
    Alation only allows for filtering by one custom field (which verification status is) at a time.
    Relevant custom fields:
        how verified field id = 10048
        verification status field id = 10049

    Notes
    -----
    There is no mechanism for explicity excluding columns which already exist in the dictionary from the request.
    Additionally, there is no way to filter by when records were added (ex give me all records entered after some date).
    As such, client-side filtering is performed within the Dictionary class to ensure no duplicate records from the API response are added to the dictionary.
    """

    def __init__(self, api_token: str):
        self.params: dict[str, str] | None = {
            "fields": "id,name,title,description",
            "custom_fields": json.dumps([ {"field_id": 10049, "value": "Approved"} ])
        }
        self.session: requests.Session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "token": api_token
        })
        self.base_url: str = "https://alation.medcity.net/integration/v2/column/"
        self.next_response_url: str | None = self.base_url

    def _get(self):
        """
        Internal Client method for performing GET request to Alation API
        """
        response = self.session.get(
            url=self.next_response_url or self.base_url,
            headers=self.session.headers,
            params=self.params,
            verify=False
        )

        response.raise_for_status()

        next_page = response.headers.get("X-Next-Page")
        self.next_response_url = (
            urljoin(self.base_url, next_page) if next_page else None
        )
        # params are set to None after the first request as they are already present in X-Next-Page urls
        self.params = None

        return [Record(**record) for record in response.json()]


    def api_response(self) -> Iterator[Record]:
        """
        Iterates through paginated API responses and yields each record.
        """
        while self.next_response_url:
            yield from self._get()
