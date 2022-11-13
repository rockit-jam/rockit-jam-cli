from argparse import ArgumentError, ArgumentParser, Namespace
from pathlib import Path
from rockit.component.graph import ComponentGraph
from rockit.component.local.reverse_proxy import ReverseProxy
from rockit.component.local.site import Site

from rockit.spec import Spec

from typing import Dict, Any
import docker

from docker.types import Mount

import yaml
import sys
import subprocess


def _execute_build(args: Namespace) -> int:
    print("local")

    spec_file = args.spec or Path("spec.yaml")
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec '{str(spec_file)}' not found.")

    spec = Spec.create_from_file(spec_file)

    spec.complete()

    cgraph = ComponentGraph.create_from_spec(spec)

    for comp in cgraph.iter_root_to_leaf():
        comp.build()

    return 0

def setup_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "spec", type=Path, nargs="?", default=Path("spec.yaml"), help="input file"
    )
    parser.set_defaults(func=_execute_local)
