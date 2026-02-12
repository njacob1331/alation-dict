import csv
from rapidfuzz import fuzz, process
from collections import defaultdict

from .record import Record
from .storage import Storage

class Dictionary:
    """
    Responsible for managing the approved column definition dictionary.
    Methods are provided to perform both direct and fuzzy lookups of records by 'name'.
    'name' corresponds to a column name in Alation.

    Note
    -
    Initializing this class will read from the specified path or create it. The path must point to a json file.
    """

    def __init__(self, storage: Storage):
        self.storage: Storage = storage
        self.index: dict[int, Record] = {}
        self.name_index: defaultdict[str, set[int]] = defaultdict(set)

        for r in self.storage.read():
            self.index[r.id] = r
            self.name_index[r.name].add(r.id)

        self._name_cache = tuple(sorted(self.name_index.keys()))

        self.new_record_count: int = 0
        self.updated_record_count: int = 0

    def records(self) -> list[Record]:
        """
        Returns all the records in the dictionary
        """
        return list(self.index.values())

    def lookup(self, lookup_value: str) -> list[Record]:
        """
        Performs a direct lookup based on the 'name' field

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        ids = self.name_index.get(lookup_value)

        return [self.index[id] for id in ids] if ids else []

    def unique(self, records: list[Record]) -> list[Record]:
        seen: set[str] = set()
        unique: list[Record] = []

        for record in records:
            if not record.description in seen:
                seen.add(record.description)
                unique.append(record)

        return unique


    def fuzzy_lookup(self, lookup_value: str, threshold: int) -> list[Record]:
        """
        Performs a fuzzy lookup based on the 'name' field. Only records with a 'name' value whose similarity score exceeds the threshold are returned.

        Note
        ----
        This method may return multiple records all of which share the same 'name' value.
        """
        search_result = process.extractOne(lookup_value, self._name_cache, scorer=fuzz.WRatio)

        if search_result is None:
            return []
        else:
            best_match, score, _ = search_result
            return self.lookup(best_match) if score >= threshold else []

    def _refresh_name_cache(self) -> None:
        self._name_cache = tuple(sorted(self.name_index.keys()))

    def add(self, record: Record) -> None:
        """
        Adds or updates records in the dictionary. Existing records are skipped.
        """
        existing = self.index.get(record.id)

        # skip existing records
        if existing == record:
            return

        # add new records
        if existing is None:
            self.index[record.id] = record
            before = len(self.name_index)
            self.name_index[record.name].add(record.id)

            if len(self.name_index) != before:
                self._refresh_name_cache()

            self.new_record_count += 1
            return

        # patch name index if our record is stale
        if existing.name != record.name:
            self.name_index[existing.name].discard(record.id)
            self.name_index[record.name].add(record.id)

            if not self.name_index[existing.name]:
                del self.name_index[existing.name]

            self._refresh_name_cache()
        else:
            self.name_index[record.name].add(record.id)

        # patch index if our record is stale
        self.index[record.id] = record
        self.updated_record_count += 1

    def _generate_insert_query(self, record: Record):
        fields = list(Record.model_fields.keys())
        cols = ", ".join(fields)
        placeholders = ", ".join([f"@{f}" for f in fields])
        values = [getattr(record, f) for f in fields]
        query = f"INSERT INTO some_table ({cols}) VALUES ({placeholders});"

        return query, values


    def export_records(self, records: list[Record], path: str) -> None:
        """
        Exports a list of records as csv to the specified path
        """
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(Record.model_fields.keys())
            for r in records:
                writer.writerow(r.model_dump().values())

    def has_updates(self) -> bool:
        return self.new_record_count > 0 or self.updated_record_count > 0

    def save(self) -> None:
        if self.has_updates():
            self.storage.write(self.records())
