from typing import Any
from alation_dict.record import Record
from alation_dict.dictionary import Dictionary
from alation_dict.storage import Storage, StorageType

"""
Patches records with the specified values. This can be combined with the PATCH /integration/v2/column/ endpoint
to perform "alignment" (ie column x is defined 10 different ways across multiple schemas and we want them all
to have a consistent title and description)
"""

# these are the changes we want to make
changes: dict[str, Any] = {
    "title": "best title",
    "description": "best description",
    "phi": "No",
    "pii": "No"
}

storage = Storage(StorageType.LOCAL_FILE, "path/to/dictionary")
dictionary = Dictionary(storage)

lookup_result = dictionary.lookup("coid")

# for every instance of coid, regardless of schema, set the
# title and description to what we have defined above
for result in lookup_result:
    print(f"\nORIGINAL:\n{result}\n\nPATCHED:\n{Record.patch(result, changes)}\n")
