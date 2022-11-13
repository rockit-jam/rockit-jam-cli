

from pathlib import Path
from rockit.spec.spec import Json
import yaml

def _load_swagger_from_file(path: Path) -> Json:
    with open(path) as f:
        ret = yaml.safe_load(f)
    return ret

class Api(object):
    name: str
    swagger: Json

    def __init__(self, name: str) -> None:
        self.name = name
        self.swagger = _load_swagger_from_file(Path(name))
