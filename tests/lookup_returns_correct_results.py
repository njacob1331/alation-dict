import os
from alation_dict import Dictionary, Record, Storage, StorageType

"""
Test to ensure that all records with a given name are returned
"""

storage = Storage(
    StorageType.LOCAL_FILE,
    "test.json"
)
dictionary = Dictionary(storage)

x = Record.model_construct(
    id=123,
    name="test",
    title="title",
    description="description",
    url="https://url.com",
    table_name="table_name",
    page_status="status",
    phi="PHI",
    pii="PII"
)

y = Record.model_construct(
    id=456,
    name="test",
    title="title",
    description="diff description",
    url="https://diff-url.com",
    table_name="diff_table_name",
    page_status="status",
    phi="PHI",
    pii="PII"
)

dictionary.add(x)
dictionary.add(y)

got = dictionary.lookup("test")
expected = [x, y]

assert sorted(got, key=lambda r: r.id) == sorted(expected, key=lambda r: r.id), (
    f"expected {expected} got {got}"
)

os.remove("test.json")
