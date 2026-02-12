from enum import Enum
import json
from pathlib import Path

from .record import Record

class StorageType(Enum):
    FILE = 0
    GCP = 1

class Storage:
    """
    Abstraction over storage options. Storage is either a file or GCP table.
    Responsibilites are limited to reading from and writing to the desired storage location.
    """
    def __init__(self, type: StorageType, path: str):
        self.type: StorageType = type
        self.path: str = path

    def read(self):
        """
        Reads from the specified storage location.
        """
        match self.type:
            case StorageType.FILE:
                return self._read_file()
            case StorageType.GCP:
                raise Exception("GCP isn't supported yet")

    def write(self, records: list[Record]):
        """
        Writes to the specified storage location.
        """
        match self.type:
            case StorageType.FILE:
                return self._write_file(records)
            case StorageType.GCP:
                raise Exception("GCP isn't supported yet")

    def _read_file(self):
        try:
            path: Path = Path(self.path)
            if not path.exists():
                _ = path.write_text('[]', encoding="utf-8")

            with open(path, "r", encoding="utf-8") as p:
                records = json.load(p)

            for record in records:
                yield Record.model_construct(**record)
        except:
            raise


    def _write_file(self, records: list[Record], write_to: str | None = None):
        output = [record.model_dump() for record in records]

        with open(write_to or self.path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False)
