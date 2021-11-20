from typing import Dict, Any

from rockit.core.spec import Spec

Json = Dict[str, Any]


class Component(object):
    _type: str
    _name: str
    _params: Json

    def __init__(self, type: str, name: str, params: Json) -> None:
        self._type = type
        self._name = name
        self._params = params

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def params(self) -> Json:
        return self._params

    def get_service_def(self, spec: Spec, components: Dict[str, "Component"]) -> Json:
        raise NotImplementedError(f"Component type {self.type} is not implemented.")
