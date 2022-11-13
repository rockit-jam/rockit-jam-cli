import networkx
from rockit.spec import Spec


class ComponentGraph(networkx.DiGraph):

    @staticmethod
    def create_from_spec(spec: Spec) -> "ComponentGraph":

        pass
