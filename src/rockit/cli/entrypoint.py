from typing import List

from argparse import ArgumentParser
import subprocess

from pathlib import Path
import os

from . import analyze
from . import local
from . import init


def entrypoint(argv: List[str]) -> int:
    print("rocket main.")

    parser = ArgumentParser(description="Process some integers.")
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    subparsers = parser.add_subparsers(help="sub-command help")

    init_parser = subparsers.add_parser("init", help="init command")
    init.setup_parser(init_parser)

    # create the parser for the "a" command
    analyze_parser = subparsers.add_parser("analyze", help="analyze command")
    analyze.setup_parser(analyze_parser)

    # create the parser for the "a" command
    local_parser = subparsers.add_parser("local", help="local help")
    local.setup_parser(local_parser)
    # parser_local.add_argument('--name', type=str, help='bar help')
    # parser_local.set_defaults(func=_exec_local)

    # # create the parser for the "b" command
    # parser_deploy = subparsers.add_parser('deploy', help='deploy help')
    # # parser_deploy.add_argument('--baz', choices='XYZ', help='baz help')
    # parser_deploy.set_defaults(func=_exec_deploy)

    print(argv)
    args = parser.parse_args(argv[1:])
    # print(args.accumulate(args.integers))
    print(args)
    if hasattr(args, "func"):
        retcode = args.func(args)
        exit(retcode)

    # with open('swagger.yaml') as f:
    #     swagger = yaml.load(f)

    # aws_lambda.Function(self, )
