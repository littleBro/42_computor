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
    Mathematics language interpreter using the Top-down operator precedence parsing algorithm.
    """
    def __init__(self, symbols=default_symbols, functions=default_functions):
        self.symbols = {x.id(): x for x in symbols}
        self.functions = functions
        self.tokens = []
        self.variables = {}
        self.text = None
        self.tokens_queue = None
        self.current_token = None
        self.result = None

    def tokenize(self):
        """
        Tokenize self.text and assign two attributes:
        - self.tokens — list of all token instances found in the text
        - self.tokens_queue — state-maintaining iterator through self.tokens
        """
        # regex will be like r'\s*(?P<NAME>[a-zA-Z]+)|(?P<NUMBER>(?:[0-9\.]+i?)|i)|(?P<PLUS>\+)|(?P<MINUS>-)'
        token_regex = r'\s*' + r'|'.join([f'(?P<{x.id()}>{x.pattern})' for x in self.symbols.values()])
        try:
            self.tokens = [
                self.symbols[match.lastgroup](self, match.group(match.lastgroup))
                for match in re.finditer(token_regex, self.text)
            ] + [End()]

            self.tokens_queue = (token for token in self.tokens)

        except KeyError:
            raise SyntaxError("Unknown operator")

    def advance(self, to_class):
        """
        Advance to the next token of given type and return the intermediate result,
        useful for handling parentheses
        """
        expr = self.expression()
        if self.current_token.id() != to_class.id():
            raise SyntaxError(f"Expected {to_class.id()}")
        self.current_token = next(self.tokens_queue)
        return expr

    def expression(self, previous_bp=0):
        """
        Recursive parsing and interpreting function.

        The previous_bp (previous binding power) parameter means the precedence level of the previous context.
        We will continue interpreting tokens while current binding power stays higher than the previous,
        then return the result to caller.

        Token classes with their semantics are defined in the parser.symbols module.
        Each token has two different modes of interpretation:

        1) prefix method returns a value for bare or prefix token position, e.g.:
            - [NUMBER]: NUMBER.prefix() will just return the token value
            - [MINUS, EXPRESSION]: MINUS.prefix() will evaluate the following EXPRESSION (next recursion level)
              and return its negated result

        2) infix method returns a value for postfix or infix token position, e.g.:
            - [..., FACTORIAL]: FACTORIAL.infix() will  receive the result of previous computations
              and return its computed factorial
            - [..., PLUS, EXPRESSION]: PLUS.infix() will receive the result of previous computations,
              evaluate the following EXPRESSION and return the sum
        """
        t = self.current_token
        self.current_token = next(self.tokens_queue)
        left = t.prefix()
        while previous_bp < self.current_token.bp:
            t = self.current_token
            self.current_token = next(self.tokens_queue)
            left = t.infix(left)
        return left

    def parse(self, text):
        """Parse and interpret current string, storing the result to self.result"""
        self.result = None
        self.text = text
        self.tokenize()
        self.current_token = next(self.tokens_queue)
        self.result = self.expression()

        if not isinstance(self.current_token, End):
            self.result = None
            raise SyntaxError(f"Unexpected token {self.current_token.id()}")

    def run(self, s=None, interactive=True):
        """Run the interpreter with user input and error handling"""
        while True:
            try:
                if interactive:
                    s = input("> ")
                    if not s:
                        continue

                self.parse(s)
                print(self.result.solution_text if isinstance(self.result, Polynomial) else self.result)

            except (MathError, ResolveError, ZeroDivisionError) as e:
                print(f"Could not compute: {e}")
            except TypeError:
                print("Could not compute: unsupported operation")
            except SyntaxError as e:
                print(f"You have an error in your syntax: {e}")
            except StopIteration:
                print("Could not parse: unexpected end of expression. Did you forget something?")
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break
            except Exception:
                print("Could not deal with it, please check your syntax")
            finally:
                if not interactive:
                    break
