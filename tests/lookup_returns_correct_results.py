import os
from alation_dict import Dictionary, Record, Storage, StorageType

"""
Test to ensure that all records with a given name are returned
"""

storage = Storage(
    StorageType.FILE,
    "test.json"
)
dictionary = Dictionary(storage)

x = Record(
    id=123,
    name="test",
    title="title",
    description="description",
    url="https://url.com"
)

y = Record(
    id=456,
    name="test",
    title="different title",
    description="different description",
    url="https://diff-url.com"
)

dictionary.add(x)
dictionary.add(y)

got = dictionary.lookup("test")
expected = [x, y]

assert sorted(got, key=lambda r: r.id) == sorted(expected, key=lambda r: r.id), (
    f"expected {expected} got {got}"
)

os.remove("test.json")
