import yaml
from pathlib import Path

from typing import Dict, Any


Json = Dict[str, Any]


class Spec(object):
    _file: Path
    _data: Json

    def __init__(self, data: Json, file: Path) -> None:
        self._file = file
        self._data = data

    @property
    def directory(self) -> Path:
        return self._file.parent

    @property
    def components(self) -> Json:
        return self._data.get("components", {})

    @staticmethod
    def create_from_file(file: Path) -> "Spec":
        with open(file) as fin:
            data = yaml.safe_load(fin)

        return Spec(data, file)

    @staticmethod
    def create_new(file: Path) -> "Spec":
        with open(file) as fin:
            data = yaml.safe_load(fin)

        return Spec(data, file)
