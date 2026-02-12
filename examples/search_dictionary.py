from alation_dict import Dictionary, Storage, StorageType

"""
Searches for a list of columns in the dictionary
"""

# first initalize the dictionary
storage = Storage(StorageType.FILE,"path/to/dictionary")
dictionary = Dictionary(storage)

# example of new columns that we want to lookup
columns_to_lookup = [
    "coid",
    "eff_timestamp",
    "street_address",
]

for column in columns_to_lookup:

    # we can do a direct lookup by column name
    lookup_result = dictionary.lookup(column)

    # if we didn't get any hits with the direct lookup, we can do a fuzzy lookup
    if len(lookup_result) == 0:
        lookup_result = dictionary.fuzzy_lookup(column, 75)

    # decide what to do with the lookup result
    # ex print all descriptions
    # we could also export if we want: dictionary.export_records(lookup_result, "export.csv")
    print(f"Query: {column}")
    for result in lookup_result:
        print(f"""
        Search Result
        -------------
        Column Name : {result.name}
        Description : {result.description}
        Source: {result.url}

        """)
