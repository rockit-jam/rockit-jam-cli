from argparse import ArgumentError, ArgumentParser, Namespace
from pathlib import Path
from rockit.core.local.reverse_proxy import ReverseProxy
from rockit.core.local.site import Site

from rockit.core.spec import Spec

from typing import Dict, Any
import docker

from docker.types import Mount

import yaml
import sys
import subprocess

Json = Dict[str, Any]


_COMPONENT_CLASS = {
    "site": Site,
    "reverse_proxy": ReverseProxy,
}


def _make_compose_def(spec: Spec) -> Json:

    components = {}

    compose_def = {"services": {}}
    for name, params in spec.components.items():
        comp_type = params.get("type")
        if comp_type is None:
            raise ArgumentError(f"Component {name} must have type parameter.")

        comp_class = _COMPONENT_CLASS.get(comp_type)
        if comp_class is None:
            raise ArgumentError(f"Component type {comp_type} for {name} is invalid.")

        comp = comp_class(name, params)
        compose_def["services"].update(comp.get_service_def(spec, components))

        components[name] = comp
        components[f"${name}"] = comp

    # rockit_temp = spec.directory / ".rockit" / "local"
    # temp = rockit_temp / "reverse_proxy"
    # temp.mkdir(parents=True, exist_ok=True)

    # default_conf_path = temp / "default.conf"
    # with open(default_conf_path, "w") as fout:
    #     print(_NGINX_CONF, file=fout)

    # compose_def["services"].update(
    #     {
    #         "reverse_proxy": {
    #             "image": "nginx:alpine",
    #             "ports": ["80:80",],
    #             "command": ["nginx", "-g", "daemon off;"],
    #             "volumes": [
    #                 {
    #                     "type": "bind",
    #                     "source": str(default_conf_path.absolute()),
    #                     "target": "/etc/nginx/conf.d/default.conf",
    #                     "read_only": True,
    #                 }
    #             ],
    #             "links": ["gui:gui_server",],
    #             "working_dir": "/home/api",
    #         },
    #     }
    # )

    # compose_def = {
    #     "services": {
    #         "gui": {
    #             "image": "node:14-alpine",
    #             # "ports": ["3000:3000",],
    #             "command": ["yarn", "dev"],
    #             "volumes": [
    #                 {
    #                     "type": "bind",
    #                     "source": str(Path(".").absolute() / "gui"),
    #                     "target": "/home/node",
    #                 }
    #             ],
    #             "user": "1000",
    #             "working_dir": "/home/node",
    #         },
    #         "api": {
    #             "image": "tiangolo/meinheld-gunicorn-flask:python3.8-alpine3.11",
    #             # "image": "nginx:alpine",
    #             "ports": ["9080:9080",],
    #             # "command": ["nginx", "-g", "daemon off;"],
    #             "volumes": [
    #                 {
    #                     "type": "bind",
    #                     "source": str(Path(".").absolute() / "api" / "src"),
    #                     "target": "/app",
    #                 },
    #                 # {
    #                 #     "type": "bind",
    #                 #     "source": str(Path(".").absolute() / "api" / "default.conf"),
    #                 #     "target": "/etc/nginx/conf.d/default.conf",
    #                 #     "read_only": True,
    #                 # },
    #             ],
    #             # "working_dir": "/home/api",
    #             # "user": "1000",
    #             "environment": {
    #                 # "HOST": "0.0.0.0",
    #                 "PORT": "9080",
    #             }
    #         },
    #         "reverse_proxy": {
    #             "image": "nginx:alpine",
    #             "ports": ["80:80",],
    #             "command": ["nginx", "-g", "daemon off;"],
    #             "volumes": [
    #                 {
    #                     "type": "bind",
    #                     "source": str(
    #                         Path(".").absolute() / "reverse_proxy" / "default.conf"
    #                     ),
    #                     "target": "/etc/nginx/conf.d/default.conf",
    #                     "read_only": True,
    #                 }
    #             ],
    #             "links": ["api:api_server", "gui:gui_server",],
    #             "working_dir": "/home/api",
    #         },
    #     },
    # }

    return compose_def


def _execute_local(args: Namespace) -> int:
    print("local")

    spec_file = args.spec or Path("spec.yaml")
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec '{str(spec_file)}' not found.")

    spec = Spec.create_from_file(spec_file)

    compose_def = _make_compose_def(spec)

    with open("docker-compose.yml", "w") as fout:
        yaml.dump(compose_def, fout)

    popen = subprocess.Popen(["docker-compose", "up"])
    while True:
        try:
            if popen.returncode is None:
                popen.wait()
            break
        except KeyboardInterrupt:
            continue
        except Exception:
            break

    return popen.returncode


def setup_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "spec", type=Path, nargs="?", default=Path("spec.yaml"), help="input file"
    )
    parser.set_defaults(func=_execute_local)
