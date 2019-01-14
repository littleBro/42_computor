"""
Home-made number data types
"""
from numbers import Number
from mathematics import abs, is_integer, parse_number, bisection
from mathematics.exceptions import MathError


class Complex(Number):
    """
    This class represents complex number data type.
    All other number types are its subclasses.
    Its real and imaginary parts are stored as python native int or float numbers
    """
    def __init__(self, make_from=0, real=0, imag=0):
        if isinstance(make_from, Complex):
            self.real = make_from.real
            self.imag = make_from.imag
        else:
            self.real = parse_number(make_from or real)
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
                real=(self.real * other.real + self.imag * other.imag) / (other.real ** 2 + other.imag ** 2),
                imag=(self.imag * other.real - self.real * other.imag) / (other.real ** 2 + other.imag ** 2)
            )
        elif isinstance(other, Number):
            return self.__truediv__(Complex(other))
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Complex):
            return Complex(
                real=(other.real * self.real + other.imag * self.imag) / (self.real ** 2 + self.imag ** 2),
                imag=(other.imag * self.real - other.real * self.imag) / (self.real ** 2 + self.imag ** 2)
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
                    return Complex(1) / self.__pow__(-power)
            elif power == 0.5 and not self.imag:
                n = abs(self.real)

                # We will use the bisection algorithm to find the roots
                # of the x^2 - n = 0 equation on the interval from 0 to n
                root = bisection(lambda x: x * x - n, 0, n)
                return Complex(real=root) if self.real >= 0 else Complex(imag=root)
        except RecursionError:
            raise MathError('Too big power')

        return NotImplemented

    def __neg__(self):
        return self * -1

    def __abs__(self):
        if self.imag:
            return self
        return abs(self.real)

    # String representation

    def __str__(self):
        real = f"{self.real:g}"
        imag = f"{abs(self.imag):g}" if abs(self.imag) != 1 else ""
        sign = '+' if self.imag > 0 else '-'

        if not self.imag:
            return real
        elif not self.real:
            return f"{sign}{imag}i"
        else:
            return f"{real} {sign} {imag}i"


class Real(Complex):
    pass


class Rational(Real):
    pass


class Integral(Rational):
    pass


class AnyRealNumber(Real):
    pass

