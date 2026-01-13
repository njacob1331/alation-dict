# Alation data dictionary
Api client and dictionary manager for storing, updating, and quickly accessing column-level records from Alation based on data governance approval criteria.

## Install Dependencies
pip install -r requirements.txt

## Install package locally
pip install -e .

## Recommended usage
examples contains a couple examples to showcase usage.

## Api client
The Api client provided is for the integration/v2/column/ endpoint. Authentication is required via Alation Api token: https://developer.alation.com/dev/docs/authentication-into-alation-apis.
In the current setup, the request parameters are set to filter for records where Verification Status = "Approved"

## Dictionary manager
The dictionary manager is responsible for handling file operations on the dictionary file, adding new records, updating existing records, and providing both direct and fuzzy lookup based on column name.
