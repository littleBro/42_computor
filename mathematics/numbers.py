"""
Home-made number data types
"""
from numbers import Number
from mathematics import abs, is_integer, parse_number, bisection, round
from mathematics.exceptions import MathError


class Complex(Number):
    def __init__(self, real=0, imag=0):
        self.real = parse_number(real)
        self.imag = parse_number(imag)

    def is_integer(self):
        return not self.imag and is_integer(self.real)

    # Comparisons

    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag
        elif isinstance(other, Number):
            return self.__eq__(Complex(other))
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Complex):
            return self.real < other.real
        elif isinstance(other, Number):
            return self.__lt__(Complex(other))
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Complex):
            return self.real <= other.real
        elif isinstance(other, Number):
            return self.__le__(Complex(other))
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Complex):
            return self.real > other.real
        elif isinstance(other, Number):
            return self.__gt__(Complex(other))
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Complex):
            return self.real >= other.real
        elif isinstance(other, Number):
            return self.__ge__(Complex(other))
        return NotImplemented

    # Math operations (left- and right-hand)

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(real=self.real + other.real, imag=self.imag + other.imag)
        elif isinstance(other, Number):
            return self.__add__(Complex(other))
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(real=self.real - other.real, imag=self.imag - other.imag)
        elif isinstance(other, Number):
            return self.__sub__(Complex(other))
        return NotImplemented

    def __rsub__(self, other):
        return other + self * -1

    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(
                real=self.real * other.real - self.imag * other.imag,
                imag=self.real * other.imag + self.imag * other.real
            )
        elif isinstance(other, Number):
            return self.__mul__(Complex(other))
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            return Complex(
                real=round((self.real * other.real + self.imag * other.imag) / (other.real ** 2 + other.imag ** 2)),
                imag=round((self.imag * other.real - self.real * other.imag) / (other.real ** 2 + other.imag ** 2))
            )
        elif isinstance(other, Number):
            return self.__truediv__(Complex(other))
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Complex):
            return Complex(
                real=round((other.real * self.real + other.imag * self.imag) / (self.real ** 2 + self.imag ** 2)),
                imag=round((other.imag * self.real - other.real * self.imag) / (self.real ** 2 + self.imag ** 2))
            )
        elif isinstance(other, Number):
            return self.__rtruediv__(Complex(other))
        return NotImplemented

    def __pow__(self, power, modulo=None):
        if modulo:
            return NotImplemented

        if self == 0 and power < 0:
            raise ZeroDivisionError('Trying to get a negative power of zero')

        try:
            if is_integer(power):
                if power == 0:
                    return Complex(1)
                if power == 1:
                    return Complex(real=self.real, imag=self.imag)
                if power > 1:
                    return self * self.__pow__(power - 1)
                if power < 0:
                    return round(Complex(1) / self.__pow__(-power))
            elif power == 0.5 and not self.imag:
                n = abs(self.real)

                # We will use the bisection algorithm to find the roots
                # of the x^2 - n = 0 equation on the interval from 0 to n
                root = round(bisection(lambda x: x * x - n, 0, n))
                return Complex(real=root) if self.real >= 0 else Complex(imag=root)
        except RecursionError:
            raise MathError('Too big power')

        return NotImplemented

    def __neg__(self):
        return self * -1

    def __abs__(self):
        return abs(self.real)

    # String representation

    def __str__(self):
        return '{real}{sign}{imag}{i}'.format(
            real=self.real if self.real or not self.imag else '',
            sign='' if not (self.real and self.imag) else ' + ' if self.imag > 0 else ' - ',
            imag=self.imag if not self.real and self.imag else abs(self.imag) if self.imag else '',
            i='i' if self.imag else ''
        )


class Real(Complex):
    pass


class Rational(Real):
    pass


class Integral(Rational):
    pass


class AnyRealNumber(Real):
    pass

