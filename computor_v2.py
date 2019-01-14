#!/usr/bin/env python

"""
Simple yet powerful mathematics language interpreter
"""
import readline
from argparse import ArgumentParser

from parser.computor import Computor


def run():
    arg_parser = ArgumentParser(description="This is a simple yet powerful mathematics language interpreter.")
    arg_parser.add_argument('expression_string', type=str, nargs='?', default=None, help="an expression to be solved")
    args = arg_parser.parse_args()

    readline.parse_and_bind('"\\C-p": previous-history')
    readline.parse_and_bind('"\\C-n": next-history')

    computor = Computor()

    if args.expression_string:
        computor.run(args.equation_string, interactive=False)
    else:
        print("Running Computor in the interactive mode")
        computor.run()


if __name__ == '__main__':
    run()
