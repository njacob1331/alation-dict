from alation_dict import Dictionary, Storage, StorageType

"""
Search the dictionary
"""

storage = Storage(StorageType.LOCAL_FILE, "path/to/dictionary")
dictionary = Dictionary(storage)

lookup_result = dictionary.lookup("coid")

# we can also do a fuzzy lookup if we don't get any results
# from the direct lookup
#
# if len(lookup_result) == 0:
#   lookup_result = dictionary.fuzzy_lookup("coid", threshold=90)

for result in lookup_result:
    print(f"""
    Search Result
    -------------
    Column Name : {result.name}
    Description : {result.description}
    Source: {result.url}

    """)
