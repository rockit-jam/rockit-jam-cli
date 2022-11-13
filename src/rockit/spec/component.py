from typing import Optional, Dict, Any

class Component(object):
    name: str  
    type: str
    using: Dict[str, "Component"]

    def __init__(self, name: str, type: str, using: Optional[Dict[str, "Component"]] = None) -> None:
        self.name = name
        self.type = type
        self.using = using or []

    @staticmethod    
    def create_from_dict(name: str, data: Dict[str, Any]) -> "Component":
        return Component(
            name=name,
            type=data["type"]
        )
