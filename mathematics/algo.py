from mathematics import DEFAULT_PRECISION, DEFAULT_ITERATIONS
from mathematics.exceptions import MathError


def bisection(fn, a, b, precision=DEFAULT_PRECISION, max_iterations=DEFAULT_ITERATIONS):
    """
    This function finds an equation root on the given interval,
    using the bisection (i.e. binary search, dichotomy) method.
    See the page https://en.wikipedia.org/wiki/Bisection_method

    :param fn: a function such that f(x) = 0, e.g. lambda x: x^2 - 4
    :param a: start endpoint, i.e. 0
    :param b: final endpoint, i.e. 4
    :param precision: acceptable precision error, i.e. 0.0000001
    :param max_iterations: maximum iterations number to prevent infinite looping
    :return: the equation root found
    """
    for i in range(0, max_iterations):
        mid = (a + b) / 2

        if fn(mid) == 0 or (b - a) / 2 < precision:
            return mid
        elif fn(mid) > 0:
            b = mid
        else:
            a = mid

    raise MathError('Could not found any solution in {} iterations'.format(max_iterations))
