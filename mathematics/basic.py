"""
Basic math operations
"""
from mathematics import DEFAULT_ERROR


def abs(a):
    return a if a >= 0 else -a


def is_integer(a):
    from mathematics.numbers import Complex

    return isinstance(a, int) or isinstance(a, (float, Complex)) and a.is_integer()


def parse_number(n):
    """Convert object number type to builtin"""
    from mathematics.numbers import Complex

    if isinstance(n, int):
        return n
    if isinstance(n, float):
        return int(n) if n.is_integer() else n
    if isinstance(n, Complex):
        if n.imag:
            raise ValueError
        return parse_number(n.real)
    if isinstance(n, str):
        return parse_number(float(n))


def round(n, precision=DEFAULT_ERROR):
    """Round 1.9999999 to 2 if necessary, regarding the precision"""
    n = parse_number(n)
    sign = -1 if n < 0 else 1

    base = int(n)
    if abs(n) + precision >= abs(base) + 1:
        return sign * (abs(base) + 1)
    elif abs(n) - precision <= abs(base):
        return base
    else:
        return n
