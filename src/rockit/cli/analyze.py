from argparse import ArgumentParser, Namespace
from pathlib import Path
from rockit.core.spec import Spec


def _execute(args: Namespace) -> int:
    print("analyze command")

    spec = Spec.create_from_file(args.file)

    print(spec.components)

    return 0


def setup_parser(parser: ArgumentParser) -> None:
    parser.add_argument(dest="file", type=Path, help="input file")
    parser.set_defaults(func=_execute)
