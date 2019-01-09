"""
Symbol classes incorporating grammar and semantics.

lbp: left binding power
nud: value returned when the symbol isn't left preceded (i.e. in bare or prefix position, e.g. x, -5)
led: value returned when the symbol is left preceded (i.e. in infix or suffix position, e.g. 5 - 2, x!)
"""
from mathematics.numbers import Real, Complex
from parser.exceptions import ResolveError
from mathematics.polynomial import Polynomial, Variable


class Symbol:
    pattern = None
    lbp = 0

    @classmethod
    def id(cls):
        return cls.__name__.upper()

    def nud(self):
        raise SyntaxError('{} symbol does not support prefix position'.format(self.id()))

    def led(self, left):
        raise SyntaxError('{} symbol does not support infix position'.format(self.id()))


# Literals

class Literal(Symbol):
    def __init__(self, parser, value):
        self.parser = parser
        self.value = self.clear(value)

    def clear(self, value):
        return value

    def nud(self):
        return self.value

    def __repr__(self):
        return "({} {})".format(self.id(), self.value)


class Name(Literal):
    pattern = r'[a-zA-Z]+'

    def nud(self):
        if self.value.lower() in self.parser.variables:
            return self.parser.variables[self.value.lower()]
        elif [x for x in self.parser.tokens if isinstance(x, Equals)]:
            variable = Variable(name=self.value, degree=1)
            self.parser.variables[self.value.lower()] = variable
            return variable

        raise ResolveError('Variable {} is not defined'.format(self.value))

    def led(self, left):
        return self.nud()


class FunctionName(Literal):
    pattern = r'[a-zA-Z]+\('

    def nud(self):
        # Interpreting:
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
        elif [x for x in self.parser.tokens if isinstance(x, Equals)]:
            return Variable(name=self.value, degree=1)

        raise ResolveError('Variable {} is not defined'.format(self.value))


class Number(Literal):
    pattern = r'[\d\.]+|[\d\.]*i'

    def clear(self, value):
        try:
            return Complex(real=0, imag=value.replace('i', '')) if 'i' in value else Real(value)
        except ValueError:
            raise SyntaxError('Wrong number: {}'.format(value))


class Constant(Literal):
    pattern = r'i'


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
        return "({} {} {})".format(self.id(), self.first, self.second)


class Plus(Operator):
    pattern = r'\+'
    lbp = 10

    def nud(self):
        self.first = self.parser.expression(100)
        self.second = None
        self.value = self.first
        return self.value

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(10)
        self.value = self.first + self.second
        return self.value


class Minus(Operator):
    pattern = r'-'
    lbp = 10

    def nud(self):
        self.first = -self.parser.expression(100)
        self.second = None
        self.value = self.first
        return self.value

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(10)
        self.value = self.first - self.second
        return self.value


class Times(Operator):
    pattern = r'\*'
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(20)
        self.value = self.first * self.second
        return self.value


class TimesMatrix(Operator):
    pattern = r'\*\*'
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(20)
        self.value = self.first * self.second
        return self.value


class Divide(Operator):
    pattern = r'/'
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(20)
        self.value = self.first / self.second
        return self.value


class Modulo(Operator):
    pattern = r'%'
    lbp = 20

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(20)
        self.value = self.first % self.second
        return self.value


class Power(Operator):
    pattern = r'\^'
    lbp = 30

    def led(self, left):
        self.first = left
        self.second = self.parser.expression(25)
        self.value = self.first ** self.second
        return self.value


class LParen(Operator):
    pattern = r'\('

    def nud(self):
        return self.parser.advance(RParen)


class RParen(Operator):
    pattern = r'\)'


class Equals(Operator):
    pattern = r'\='
    lbp = 1

    def led(self, left):
        self.first = left
        self.second = self.parser.expression()
        polynomial = Polynomial(self.first) - Polynomial(self.second)
        self.value = polynomial
        return self.value


# Catch all other things

class UndefinedToken(Symbol):
    pattern = r'[^\s]+'

    def __init__(self, parser, value):
        raise SyntaxError('Unknown token {}'.format(value))


# End symbol

class End(Symbol):
    pass
