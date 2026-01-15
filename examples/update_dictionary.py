from alation_dict import Client, Dictionary

"""
Updates the dictionary based on the records contained in the Alation API response.
This script is intended to be ran as a scheduled job.
"""

# api token info: https://developer.alation.com/dev/docs/authentication-into-alation-apis
api_token = "<YOUR API TOKEN>"

dictionary = Dictionary(path="path/to/dictionary")
client = Client(api_token, config_path="path/to/config")

for record in client.api_response():
    dictionary.add(record)

dictionary.save()
