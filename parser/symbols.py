"""
Symbol classes incorporating grammar and semantics.

bp: binding power
prefix: value returned when the symbol isn't left preceded (in bare or prefix position, e.g. x, -5)
infix: value returned when the symbol is left preceded (in infix or suffix position, e.g. 5 - 2, x!)
"""
from mathematics.constants import CONSTANTS
from mathematics.matrix import Matrix
from mathematics.numbers import Real, Complex
from parser.exceptions import ResolveError
from mathematics.polynomial import Polynomial, Variable


class Symbol:
    """Parent class for all symbols"""
    pattern = None
    bp = 0

    @classmethod
    def id(cls):
        return cls.__name__.upper()

    def prefix(self):
        raise SyntaxError(f"{self.id()} symbol does not support prefix position")

    def infix(self, left):
        raise SyntaxError(f"{self.id()} symbol does not support infix position")


# Literals

class Literal(Symbol):
    def __init__(self, parser, value):
        self.parser = parser
        self.value = self.clear(value)

    def clear(self, value):
        return value

    def prefix(self):
        return self.value

    def __repr__(self):
        return f"({self.id()} {self.value})"


class Name(Literal):
    pattern = r'[a-zA-Z]+'

    def prefix(self):
        if self.value.lower() in self.parser.variables:
            return self.parser.variables[self.value.lower()]
        elif any(isinstance(x, Equals) for x in self.parser.tokens):
            variable = Variable(name=self.value, degree=1)
            self.parser.variables[self.value.lower()] = variable
            return variable

        raise ResolveError(f"Variable {self.value} is not defined")

    def infix(self, left):
        return self.prefix()


class FunctionName(Literal):
    pattern = r'[a-zA-Z]+\('

    def prefix(self):
        # TODO: Interpreting
        # get value from the parentheses
        # next token == rparen or throw
        # substitute, compute the body

        # Storing:
        # get variable from next token
        # if next is not variable, throw
        # if var is defined, throw
        # next token should be RParen, advance or throw
        # next token should be equals
        # all the rest = polynomial (or expression? or ast? or as lambda?)
        # ensure that there is only one variable == function variable
        # store the polynomial
        if self.value in self.parser.functions:
            return self.parser.variables[self.value]
        elif any(isinstance(x, Equals) for x in self.parser.tokens):
            return Variable(name=self.value, degree=1)

        raise ResolveError(f"Variable {self.value} is not defined")


class Number(Literal):
    pattern = r'(?:[0-9\.]+i?)|i'

    def clear(self, value):
        try:
            return Complex(real=0, imag=value.replace('i', '')) if 'i' in value else Real(value)
        except ValueError:
            raise SyntaxError(f"Wrong number: {value}")


class Constant(Literal):
    pattern = r'|'.join(CONSTANTS.keys())


class Needle(Literal):
    pattern = r'\?'


# Operators

class Operator(Symbol):
    def __init__(self, parser, _value):
        self.parser = parser
        self.first = None
        self.second = None
        self.value = None

    def __repr__(self):
        return f"({self.id()} {self.first} {self.second})"


class Plus(Operator):
    pattern = r'\+'
    bp = 10

    def prefix(self):
        self.first = self.parser.expression(100)
        self.second = None
        self.value = self.first
        return self.value

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first + self.second
        return self.value


class Minus(Operator):
    pattern = r'-'
    bp = 10

    def prefix(self):
        self.first = -self.parser.expression(100)
        self.second = None
        self.value = self.first
        return self.value

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first - self.second
        return self.value


class Times(Operator):
    pattern = r'\*'
    bp = 20

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first * self.second
        return self.value


class TimesMatrix(Operator):
    pattern = r'\*\*'
    bp = 20

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first * self.second
        return self.value


class Divide(Operator):
    pattern = r'/'
    bp = 20

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first / self.second
        return self.value


class Modulo(Operator):
    pattern = r'%'
    bp = 20

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(self.bp)
        self.value = self.first % self.second
        return self.value


class Power(Operator):
    pattern = r'\^'
    bp = 30

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression(25)
        self.value = self.first ** self.second
        return self.value


class LParen(Operator):
    pattern = r'\('

    def prefix(self):
        return self.parser.advance(RParen)


class RParen(Operator):
    pattern = r'\)'


class Equals(Operator):
    pattern = r'\='
    bp = 1

    def infix(self, left):
        self.first = left
        self.second = self.parser.expression()
        self.value = Polynomial(self.first) - Polynomial(self.second)
        return self.value


# Catch all other things

class UndefinedToken(Symbol):
    pattern = r'[^\s]+'

    def __init__(self, parser, value):
        raise SyntaxError(f"Unknown token {value}")


# End symbol

class End(Symbol):
    pass
