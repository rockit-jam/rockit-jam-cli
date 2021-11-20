import json
from pathlib import Path
from typing import Any, Dict

from rockit.core.component import Component
from rockit.core.spec import Spec

Json = Dict[str, Any]


def _find_command(directory: Path, command_type: str) -> str:
    package_json_path = directory / "package.json"

    if not package_json_path.exists():
        raise FileNotFoundError("package json not found.")

    with open(package_json_path) as fin:
        package_json = json.load(fin)

    for key in package_json.get("scripts", {}).keys():
        if key == command_type:
            return key
        if key.endswith(f":{command_type}"):
            return key

    raise ValueError(f"commmand {command_type} is missing in package.json.")


class Site(Component):
    def __init__(self, name: str, params: Json) -> None:
        super().__init__("site", name, params)

    def get_service_def(self, spec: Spec, components: Dict[str, Component]) -> Json:
        source = Path(self.params.get("source", self.name)).absolute()

        command = _find_command(source, "dev")

        return {
            self.name: {
                "image": "node:14-alpine",
                "ports": ["3000:3000"],
                "command": ["yarn", command, "--host", "0.0.0.0"],
                "volumes": [
                    {
                        "type": "bind",
                        "source": str(source.absolute()),
                        "target": "/home/node",
                    }
                ],
                "user": "1000",
                "working_dir": "/home/node",
            }
        }
