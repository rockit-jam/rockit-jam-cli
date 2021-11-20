from typing import Any, Dict

from rockit.core.component import Component
from rockit.core.spec import Spec

Json = Dict[str, Any]


_NGINX_CONF = """
upstream {origin}_server {{
    server {origin}_server:3000;
}}

server {{
    listen       80;
    server_name  localhost;

    location / {{
        proxy_pass http://{origin}_server;
    }}
}}
"""


class ReverseProxy(Component):
    def __init__(self, name: str, params: Json) -> None:
        super().__init__("reverse_proxy", name, params)

    def get_service_def(self, spec: Spec, components: Dict[str, Component]) -> Json:

        origin_name = self.params["routes"][0]["origin"]
        link_to = components.get(origin_name)
        if link_to is None:
            raise ValueError(f"Origin {origin_name} is not found.")

        rockit_temp = spec.directory / ".rockit" / "local"
        temp = rockit_temp / "reverse_proxy"
        temp.mkdir(parents=True, exist_ok=True)

        default_conf_path = temp / "default.conf"
        with open(default_conf_path, "w") as fout:
            print(_NGINX_CONF.format(origin=link_to.name), file=fout)

        return {
            "reverse_proxy": {
                "image": "nginx:alpine",
                "ports": ["80:80"],
                "command": ["nginx", "-g", "daemon off;"],
                "volumes": [
                    {
                        "type": "bind",
                        "source": str(default_conf_path.absolute()),
                        "target": "/etc/nginx/conf.d/default.conf",
                        "read_only": True,
                    }
                ],
                "links": [f"{link_to.name}:{link_to.name}_server"],
                "working_dir": "/home/api",
            },
        }
