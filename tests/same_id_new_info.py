import os
from alation_dict import Dictionary, Record, Storage, StorageType

"""
Test to ensure that if a record with id "n" has fields whose values have changed,
the indicies update properly to ensure the validity of lookups
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
    id=123,
    name="test",
    title="new title",
    description="new description",
    url="https://new-url.com"
)

# this adds x
dictionary.add(x)
# this should update x with y
dictionary.add(y)

assert dictionary.lookup("test") == [y], f"expected {[y]} got {dictionary.lookup("test")}"
assert dictionary.updated_record_count == 1, "expected updated_record_count == 1"

os.remove("test.json")
