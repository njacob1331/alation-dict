from alation_dict import Dictionary

"""
Searches for a list of columns in the dictionary
"""

dictionary = Dictionary("path/to/dictionary")
columns_to_search = [
    "coid",
    "iplan",
    "discharge_date",
    "net_revenue"
]

for column in columns_to_search:
    lookup_result = dictionary.lookup(column)

    # if we didn't get any hits with the direct lookup, we can do a fuzzy lookup
    if len(lookup_result) == 0:
        lookup_result = dictionary.fuzzy_lookup(column, threshold=90)

    # decide what to do with the lookup result
    # ex print all descriptions
    print([(result.name, result.description) for result in lookup_result])
