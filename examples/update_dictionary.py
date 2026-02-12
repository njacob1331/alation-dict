from alation_dict import Client, Dictionary, Storage, StorageType

"""
Updates the dictionary based on the records contained in the Alation API response.
This script is intended to be ran as a scheduled job.
"""

# auth info: https://developer.alation.com/dev/docs/authentication-into-alation-apis
auth_token = "<YOUR API TOKEN>"

# api client for making requests to Alation
client = Client(auth_token)
# specifies where we want to read from and write to
storage = Storage(StorageType.FILE, "path/to/dictionary")
# builds a searchable dictionary from the raw records
dictionary = Dictionary(storage)

for record in client.api_response():
    dictionary.add(record)

dictionary.save()
