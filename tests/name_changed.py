import os
from alation_dict import Dictionary, Record, Storage, StorageType

"""
Test to ensure that if a record with id "n" has a name which changes,
the index for the old name no longer contains said record and
the index for the new name now contains said record
"""

storage = Storage(
    StorageType.LOCAL_FILE,
    "test.json"
)
dictionary = Dictionary(storage)

x = Record.model_construct(
    id=123,
    name="name",
    title="title",
    description="description",
    url="https://url.com",
    table_name="table_name",
    page_status="status",
    phi="PHI",
    pii="PII"
)

y = Record.model_construct(
    id=123,
    name="new name",
    title="title",
    description="description",
    url="https://url.com",
    table_name="table_name",
    page_status="status",
    phi="PHI",
    pii="PII"
)

dictionary.add(x)
dictionary.add(y)

assert dictionary.lookup("name") == [], f"expected {[]} got {dictionary.lookup("name")}"
assert dictionary.lookup("new name") == [y], f"expected {[y]} got {dictionary.lookup("new name")}"

os.remove("test.json")
