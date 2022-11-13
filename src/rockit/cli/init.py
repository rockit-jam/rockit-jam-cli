from argparse import ArgumentParser, Namespace
from pathlib import Path
from rockit.spec import Spec


def _execute(args: Namespace) -> int:
    print("init command")

    spec = Spec.create_from_file(args.file)

    print(spec.components)

    return 0


def setup_parser(parser: ArgumentParser) -> None:
    parser.add_argument("--name", type=str, help="Application Name")
    parser.add_argument("--provider", type=str, help="Provider Name")
    parser.set_defaults(func=_execute)
