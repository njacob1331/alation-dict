import json
from datetime import datetime, UTC
from pathlib import Path
from typing import TypedDict, cast
from rapidfuzz import process
from collections import defaultdict

from .record import Record

class RawRecord(TypedDict):
    id: int
    name: str
    title: str
    description: str


class DictionaryFile(TypedDict):
    last_update: str
    data: list[RawRecord]

class Dictionary:
    """
    Responsible for managing the approved column definition dictionary from Alation.
    Methods are provided to perform both direct and fuzzy lookups of records by 'name'.
    'name' corresponds to a column name in Alation.

    Note
    -
    Initializing this class will read from the specified path or create it. The path must point to a json file.
    """

    def __init__(self, path: str):
        file = Path(path)

        if not file.exists():
            _ = file.write_text('{"last_update": "", "data": []}', encoding="utf-8")

        with open(file, "r", encoding="utf-8") as dictionary:
            records = cast(DictionaryFile, json.load(dictionary))

        self.file: Path = file
        self.index: dict[int, Record] = {}
        self.name_index: defaultdict[str, list[Record]] = defaultdict(list)

        for raw in records["data"]:
            r = Record(**raw)
            self.index[r.id] = r
            self.name_index[r.name].append(r)

        self.new_record_count: int = 0
        self.updated_record_count: int = 0

    def records(self):
        """
        Returns all the records in the dictionary
        """
        return list(self.index.values())

    def lookup(self, lookup_value: str):
        """
        Performs a direct lookup based on the 'name' field

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        return self.name_index.get(lookup_value) or []

    def fuzzy_lookup(self, lookup_value: str, threshold: int) -> list[Record]:
        """
        Performs a fuzzy lookup based on the 'name' field. Only records with a 'name' value whose similarity score exceeds the threshold are returned.

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        options = set(self.name_index.keys())
        search_result = process.extractOne(lookup_value, options)

        if search_result is None:
            return []
        else:
            best_match, score, _ = search_result
            return self.lookup(best_match) if score > threshold else []

    def add(self, record: Record):
        """
        Adds or updates records in the dictionary. Existing records are skipped
        """
        lookup = self.index.get(record.id)

        if lookup is None:
            self.index[record.id] = record
            self.name_index[record.name].append(record)
            self.new_record_count += 1
        elif lookup != record:
            self.index[record.id] = record
            self.name_index[record.name].append(record)
            self.updated_record_count += 1

    def save(self):
        """
        Writes to the dictionary file only if new records were added or existing records were updated.
        """
        if self.new_record_count > 0 or self.updated_record_count > 0:
            output = {
                "last_update": datetime.now(UTC).isoformat(),
                "data": [record.model_dump() for record in self.index.values()]
            }

            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
