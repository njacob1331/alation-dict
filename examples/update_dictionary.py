from alation_dict.dictionary import Dictionary
from alation_dict.client import Client, Endpoint
from alation_dict.storage import Storage, StorageType

"""
Builds/updates the dictionary based on the records contained in the Alation API response.
"""

# auth info: https://developer.alation.com/dev/docs/authentication-into-alation-apis
auth_token = "<YOUR_API_TOKEN>"

client = Client(auth_token)
storage = Storage(StorageType.FILE, "path/to/dictionary")
dictionary = Dictionary(storage)

for record in client.get(Endpoint.COLUMN):
    dictionary.add(record)

dictionary.save()
