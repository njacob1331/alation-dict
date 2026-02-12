import os
from alation_dict import Dictionary, Record, Storage, StorageType

"""
Test to ensure no duplicate records get added
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
    title="title",
    description="description",
    url="https://url.com"
)

# this adds x
dictionary.add(x)
# this should be skipped
dictionary.add(y)

assert len(dictionary.records()) == 1, "expected total record length of 1"
assert len(dictionary.lookup("test")) == 1, "expected 1 record"
assert dictionary.new_record_count == 1, "expected new_record_count == 1"
assert dictionary.updated_record_count == 0, "expected updated_record_count == 0"

os.remove("test.json")
