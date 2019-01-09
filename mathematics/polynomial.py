"""
Polynomial
Term
Variable
"""
from collections import namedtuple
from functools import reduce
from itertools import groupby
from numbers import Number

from mathematics import is_integer
from mathematics.exceptions import MathError
from mathematics.numbers import AnyRealNumber, Complex
from parser.exceptions import ResolveError


class Polynomial:
    """
    This class represents a polynomial expression.

    For the 25 + 3x - x^2 polynomial there will be following data structure:

    terms: [
        Term(25, []),
        Term(3, [Variable('x', 1)]),
        Term(-1, [Variable('x', 2)]),
    ]
    degree: 2
    variables: ['x']
    """

    def __init__(self, make_from=None, terms=None):
        if make_from is not None:
            if isinstance(make_from, Polynomial):
                self.terms = make_from.terms
            elif isinstance(make_from, Variable):
                self.terms = [Term(coeff=1, variables=[make_from])]
            elif isinstance(make_from, Number):
                self.terms = [Term(coeff=make_from, variables=[])]
            else:
                raise TypeError("Cannot build a polynomial object from {}".format(make_from))
        elif terms:
            self.terms = terms
        else:
            raise TypeError("Could not build a polynomial object")

    @property
    def terms_normalized(self):
        return [term for term in [
            Term(coeff=reduce(lambda a, x: a + x.coeff, list(group), 0), variables=key)
            for key, group in groupby(
                iterable=sorted([x for x in self.terms if x.coeff != 0], key=lambda x: x.variables_normalized),
                key=lambda x: x.variables_normalized
            )
        ] if term.coeff != 0]

    def get_term(self, degree):
        try:
            if degree == 0:
                return next((x for x in self.terms_normalized if not x.variables or x.variables[0].degree == 0))
            else:
                return next((x for x in self.terms_normalized if x.variables and x.variables[0].degree == degree))
        except StopIteration:
            return Term(coeff=0, variables=[])

    @property
    def degree(self):
        return max([term.degree for term in self.terms_normalized], default=0)

    @property
    def variables(self):
        return list(set([variable.name
                         for term in self.terms_normalized
                         for variable in term.variables]))

    @property
    def a(self):
        return Complex(self.get_term(degree=2).coeff)

    @property
    def b(self):
        return Complex(self.get_term(degree=1).coeff)

    @property
    def c(self):
        return Complex(self.get_term(degree=0).coeff)

    @property
    def D(self):
        return Complex(self.b ** 2 - 4 * self.a * self.c)

    def resolve(self):
        if len(self.variables) > 1:
            raise ResolveError("Cannot solve polynomials with multiple variables")

        if len([x for x in self.terms_normalized if x.has_unsupported_degrees]) > 0:
            raise ResolveError("Cannot solve polynomials with non-natural degrees")

        if self.degree == 0:
            return AnyRealNumber() if self.c == 0 else None

        if self.degree == 1:
            return -self.c / self.b

        if self.degree == 2:
            return (
                (-self.b + self.D ** 0.5) / (2 * self.a),
                (-self.b - self.D ** 0.5) / (2 * self.a),
            )

        if self.degree > 2:
            raise ResolveError("The polynomial degree is strictly greater than 2, I can't solve.")

        raise ResolveError("Cannot solve polynomials of degree {}".format(self.degree))

    # Math operations (left- and right-hand)

    def __add__(self, other):
        return Polynomial(terms=self.terms + Polynomial(other).terms)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + Polynomial(other) * -1

    def __rsub__(self, other):
        return Polynomial(other) + self * -1

    def __mul__(self, other):
        try:
            return Polynomial(terms=[
                a_term * b_term
                for a_term in self.terms
                for b_term in Polynomial(other).terms
            ])
        except:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Polynomial(terms=[
                Term(coeff=coeff / other, variables=variables) for coeff, variables in self.terms
            ])
        elif isinstance(other, Polynomial):
            if len(other.terms_normalized) == 0:
                raise ZeroDivisionError()
            if len(other.terms_normalized) > 1:
                raise MathError('Cannot divide by a polynomial with multiple terms')

            return Polynomial(terms=[term / other.terms[0] for term in self.terms])
        else:
            return self.__truediv__(Polynomial(other))

    # String representation

    def __str__(self):
        return ' '.join(['{sign}{space}{coeff}{asterisk}{variables}'.format(
            sign='-' if term.coeff < 0 else '' if index == 0 else '+',
            space='' if index == 0 else ' ',
            coeff=abs(term.coeff) if not (abs(term.coeff) == 1 and term.variables and term.degree != 0) else '',  # TODO
            asterisk=' * ' if abs(term.coeff) != 1 and term.variables and term.degree != 0 else '',
            variables=' * '.join([str(variable) for variable in term.variables_normalized]),
        ) for index, term in enumerate(self.terms_normalized)]) or '0'

    @property
    def solution_text(self):
        try:
            if self.degree == 2:
                if self.D > 0:
                    solution = "Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(
                        *self.resolve())
                elif self.D == 0:
                    solution = "Discriminant is zero, the solution is:\n{}".format(self.resolve()[0])
                else:
                    solution = "Discriminant is strictly negative, the two solutions are:\n{}\n{}".format(
                        *self.resolve())

            elif self.degree == 0:
                if isinstance(self.resolve(), AnyRealNumber):
                    solution = "All real numbers are solutions"
                    exceptions = list(set([variable.name
                                           for term in self.terms
                                           for variable in term.variables
                                           if variable.degree < 0]))
                    if exceptions:
                        solution += ", except " + ', '.join(['{}=0'.format(x) for x in exceptions])
                else:
                    solution = "This equation has no solutions in our world."

            else:
                solution = "The solution is:\n{}".format(self.resolve())

        except ResolveError as e:
            solution = str(e)

        return 'Reduced form: {polynomial} = 0\nPolynomial degree: {degree}\n{solution}'.format(
            polynomial=self,
            degree=self.degree,
            solution=solution,
        )


class Term(namedtuple('Term', ['coeff', 'variables'])):

    @property
    def degree(self):
        if self.coeff == 0:
            return 0
        return max([variable.degree for variable in self.variables], default=0)

    @property
    def has_unsupported_degrees(self):
        return len([variable.degree
                    for variable in self.variables
                    if not is_integer(variable.degree) or variable.degree < 0]) > 0

    @property
    def variables_normalized(self):
        return [variable for variable in [
            Variable(name=key, degree=reduce(lambda a, x: a + x.degree, list(group), 0))
            for key, group in groupby(
                iterable=sorted([x for x in self.variables if x.degree != 0], key=lambda x: x.name),
                key=lambda x: x.name
            )
        ] if variable.degree != 0]

    # Math operations (left- and right-hand)

    def __mul__(self, other):
        if isinstance(other, Term):
            return Term(
                coeff=self.coeff * other.coeff,
                variables=self.variables + other.variables
            )
            # coeff = self.coeff * other.coeff
            # variables = [
            #     Variable(name=key, degree=reduce(lambda a, x: a + x.degree, list(group), 0))
            #     for key, group in groupby(
            #         sorted(self.variables + other.variables, key=lambda x: x.name),
            #         key=lambda x: x.name
            #     )
            # ]
            # return Term(coeff, variables)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Term):
            return Term(
                coeff=self.coeff / other.coeff,
                variables=self.variables + [
                    Variable(name=x.name, degree=-x.degree) for x in other.variables
                ]
            )
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented


class Variable(namedtuple('Variable', ['name', 'degree'])):

    # Math operations (left- and right-hand)

    def __add__(self, other):
        return Polynomial(self) + other

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Polynomial(self) - other

    def __rsub__(self, other):
        return Polynomial(other) - self

    def __mul__(self, other):
        return Polynomial(self) * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Polynomial(self) / other

    def __rtruediv__(self, other):
        return Polynomial(other) / self

    def __pow__(self, power, modulo=None):
        if isinstance(power, Number):
            return Variable(name=self.name, degree=self.degree * power)
        return NotImplemented

    # String representation

    def __str__(self):
        if self.degree == 0:
            return '1'
        if self.degree == 1:
            return self.name
        return '{}^{}'.format(self.name, self.degree)
