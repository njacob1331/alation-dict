from alation_dict import Dictionary

"""
Searches for a list of columns in the dictionary
"""

dictionary = Dictionary("path/to/dictionary")
columns_to_search = [
    "coid",
    "eff_timestamp",
    "street_address_1"
]

for column in columns_to_search:

    # we can do a direct lookup by column name
    lookup_result = dictionary.lookup(column)

    # if we didn't get any hits with the direct lookup, we can do a fuzzy lookup
    if len(lookup_result) == 0:
        lookup_result = dictionary.fuzzy_lookup(column, threshold=75)

    # decide what to do with the lookup result
    # ex print all descriptions
    for result in lookup_result:
        print(f"Lookup value: {column}")
        print(f"Column name: {result.name}")
        print(f"Description: {result.description}")
        print("\n")
