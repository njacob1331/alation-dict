from typing import Any
from alation_dict import Client, Endpoint

"""
Patches records with the specified values. The record that is linked
will have its title and description changed to whats specified.
"""

TEST_ID = 12345

# these are the changes we want to make
changes: dict[str, Any] = {
    "id": TEST_ID,
    "title": "best title",
    "description": "best description"
}

auth_token = "<YOUR_API_TOKEN>"

client = Client(auth_token)
client.patch(Endpoint.COLUMN, changes)

# if we were going to do this with multiple values, we could query the dictionary
# to get all the necessary info

# storage = Storage(StorageType.FILE, "path/to/dictionary")
# dictionary = Dictionary(storage)

# for some in dictionary.lookup("something"):
#     changes["id"] = some.id

#     client.patch(Endpoint.COLUMN, changes)
