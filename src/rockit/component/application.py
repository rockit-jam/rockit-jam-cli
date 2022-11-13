from . import Component

class Application(Component):
    name: str

    def __init__(self) -> None:
        self.name = "sample_app"
