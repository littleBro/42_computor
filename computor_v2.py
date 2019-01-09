#!/usr/bin/env python

import readline
from argparse import ArgumentParser
from parser.computor import Computor


def run():
    arg_parser = ArgumentParser(description="This is a simple yet functional math interpreter")
    arg_parser.add_argument('--debug', action='store_true', help="debug mode")
    args = arg_parser.parse_args()

    readline.parse_and_bind('"\\C-p": previous-history')
    readline.parse_and_bind('"\\C-n": next-history')

    computor = Computor()
    computor.run()


if __name__ == '__main__':
    run()
