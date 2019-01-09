"""
Resolve algo:
if = is present
    if left is function
        ignore variables
        check that at right there is only one variable matching that of the function
        assign (handle the scope, don't mix later)
    elif left is variable (and right is not polynomial)
        substitute variables on the right
        resolve right, assign
    else
        resolve as Polynome_left - Polynome_right = 0
else
    substitute variables
    resolve
"""
import re

import mathematics
from mathematics.exceptions import MathError
from parser.symbols import *


default_symbols = (
    Name, FunctionName, Number, Constant, Needle,
    Plus, Minus, Times, Divide, Modulo, Power,
    LParen, RParen,
    Equals,
    UndefinedToken,
)

default_functions = {
    'abs': mathematics.abs,
}


class Computor:
    """
    Mathematics language interpreter
    """
    def __init__(self, symbols=default_symbols, functions=default_functions):
        self.symbols = {x.id(): x for x in symbols}
        self.functions = functions
        self.token_regex = r'\s*' + r'|'.join([r'(?P<{}>{})'.format(x.id(), x.pattern) for x in symbols])
        self.tokens = []
        self.variables = {}
        self.text = None
        self.tokens_queue = None
        self.current_token = None
        self.result = None

    def tokenize(self):
        try:
            self.tokens = [
                self.symbols[match.lastgroup](self, match.group(match.lastgroup))
                for match in re.finditer(self.token_regex, self.text)
            ] + [End()]

            self.tokens_queue = (token for token in self.tokens)

        except KeyError:
            raise SyntaxError("Unknown operator")

    def expression(self, rbp=0):
        t = self.current_token
        self.current_token = next(self.tokens_queue)
        left = t.nud()
        while rbp < self.current_token.lbp:
            t = self.current_token
            self.current_token = next(self.tokens_queue)
            left = t.led(left)
        return left

    def advance(self, to_class):
        expr = self.expression()
        if self.current_token.id() != to_class.id():
            raise SyntaxError("Expected {}".format(to_class.id()))
        self.current_token = next(self.tokens_queue)
        return expr

    def parse(self, text):
        self.result = None
        self.text = text
        self.tokenize()
        self.current_token = next(self.tokens_queue)
        self.result = self.expression()

        if not isinstance(self.current_token, End):
            self.result = None
            raise SyntaxError("Unexpected token {}".format(self.current_token.id()))

    def run(self, s=None, interactive=True):
        while True:
            try:
                if interactive:
                    s = input("> ")
                    if not s:
                        continue

                self.parse(s)
                print(self.result.solution_text if isinstance(self.result, Polynomial) else self.result)

            except (MathError, ResolveError, ZeroDivisionError) as e:
                print("Could not compute: {}".format(e))
            except TypeError:
                print("Could not compute: unsupported operation")
            except SyntaxError as e:
                print("You have an error in your syntax: {}".format(e))
            except StopIteration:
                print("Could not parse: unexpected end of expression. Did you forget something?")
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break
            # except Exception:
            #     print("Could not deal with it, please check your syntax")
            finally:
                if not interactive:
                    break
