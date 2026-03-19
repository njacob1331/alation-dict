import json
from enum import Enum
from pathlib import Path

from .record import Record

class StorageType(Enum):
    """
    Supported storage options

    Notes
    -
    This may be unecessary (ie we only ever want to read from and write to a
    json file in a GCP bucket). At least during dev and in the current state it
    provides added flexibility.

    Since enums can carry values, this would make it easy to carry auth credentials
    in variants that need them to pass them downstream to read and write methods

    ex: CLOUD_FILE = {"bucket": "some_bucket", "auth": "creds"}
    """
    LOCAL_FILE = 0
    CLOUD_FILE = 1
    DB = 2

class Storage:
    """
    Abstraction over storage options. Responsibilites are limited to
    reading from and writing to the desired storage location.
    """
    def __init__(self, type: StorageType, path: str):
        self.type: StorageType = type
        self.path: str = path

    def read(self):
        """
        Reads from the specified storage location.
        """
        match self.type:
            case StorageType.LOCAL_FILE:
                return self._read_local_file()
            case StorageType.CLOUD_FILE:
                raise Exception("cloud file not supported yet")
            case StorageType.DB:
                raise Exception("db not supported yet")

    def write(self, records: list[Record]):
        """
        Writes to the specified storage location.
        """
        match self.type:
            case StorageType.LOCAL_FILE:
                return self._write_local_file(records)
            case StorageType.CLOUD_FILE:
                raise Exception("cloud file not supported yet")
            case StorageType.DB:
                raise Exception("db not supported yet")

    def _read_local_file(self):
        try:
            path: Path = Path(self.path)
            if not path.exists():
                _ = path.write_text('[]', encoding="utf-8")

            with open(path, "r", encoding="utf-8") as p:
                records = json.load(p)

            for record in records:
                yield Record.model_construct(**record)
        except:
            raise Exception(f"failed to read file at path {self.path}")

    def _write_local_file(self, records: list[Record], write_to: str | None = None):
        output = [record.model_dump() for record in records]

        with open(write_to or self.path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False)

    def _read_cloud_file(self):
        pass

    def _write_cloud_file(self):
        pass

    def _read_db(self):
        pass

    def _write_db(self):
        pass
