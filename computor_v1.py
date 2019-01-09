#!/usr/bin/env python

"""
Simple program for finding polynomial roots
"""
import readline
from argparse import ArgumentParser

from parser.computor import Computor
from parser.symbols import *

symbols = (
    Name, Number,
    Plus, Minus, Times, Divide, Power,
    LParen, RParen,
    Equals,
    UndefinedToken,
)


def run():
    arg_parser = ArgumentParser(description="This program computes simple polynomial equations.")
    arg_parser.add_argument('equation_string', type=str, nargs='?', default=None, help="an equation to be solved")
    args = arg_parser.parse_args()

    readline.parse_and_bind('"\\C-p": previous-history')
    readline.parse_and_bind('"\\C-n": next-history')

    computor = Computor(symbols=symbols)

    if args.equation_string:
        computor.run(args.equation_string, interactive=False)
    else:
        print("Running Computor in the interactive mode")
        computor.run()


if __name__ == '__main__':
    run()
