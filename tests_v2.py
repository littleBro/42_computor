"""
TODO:
Assignment of an expression to a variable by type inference
Reassignment of an existing variable with an expression of another type
Assignment of a variable to another variable (existing or not)
Resolution of a mathematical expression with or without defined variable (s)
Resolution of an equation of degree less than or equal to 2
Operations between types, as much as possible
Rational numbers (for any x ∈ Q)
Imaginary numbers for any x = a + ib such as (a, b) ∈ Q^2
Matrices
Functions
Variable reassign
Variable types, type inference
needle and p.9 strange synthax
multiple solutions (operations on tuples?)
abs of complex numbers with imag
variable reassignment
in case of error (e.g. zero division), check variables to not have changed
- unicode names?

Polynomials:
- positive rational powers
- negative rational powers (attention with 0!)
- big degrees (bisection)
- x^0.83
"""

import unittest

from computor_v1 import symbols
from mathematics.polynomial import Polynomial
from parser.computor import Computor

computor = Computor(symbols=symbols)


def compute(s):
    computor.run(s, interactive=False)
    return str(computor.result.solution_text if isinstance(computor.result, Polynomial) else computor.result)


DEGREE = "Polynomial degree: {}"
REDUCED = "Reduced form: {}"
D_POSITIVE = "Discriminant is strictly positive, the two solutions are:"
D_NEGATIVE = "Discriminant is strictly negative, the two solutions are:"
D_ZERO = "Discriminant is zero, the solution is:"
D_NONE = "The solution is:"
BIG_DEGREE = "The polynomial degree is strictly greater than 2, I can't solve."
SMALL_DEGREE = "The polynomial degree is strictly less than 0, I can't solve."
ALL_NUMBERS = "All real numbers are solutions."
NO_SOLUTION = "This equation has no solutions in our world."


class TestComputor(unittest.TestCase):

    def test_correct_input(self):
        cases = [
            {
                'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
                'messages': [
                    REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '0.90523',
                    '-0.47513',
                ]
            },
            {
                'input': '5 * X^0 + 13 * X^1 + 3 * X^2 = 1 * X^0 + 1 * X^1',
                'messages': [
                    REDUCED.format('4 + 12 * X + 3 * X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '-3.6329',
                    '-0.3670',
                ]
            },
            {
                'input': '5 * X^0 + 3 * X^1 + 3 * X^2 = 1 * X^0 + 0 * X^1',
                'messages': [
                    REDUCED.format('4 + 3 * X + 3 * X^2 = 0'),
                    DEGREE.format(2),
                    D_NEGATIVE,
                    '-0.5 + 1.040832', 'i',
                    '-0.5 - 1.040832', 'i',
                ]
            },
            {
                'input': '6 * X^0 + 11 * X^1 + 5 * X^2 = 1 * X^0 + 1 * X^1',
                'messages': [
                    REDUCED.format('5 + 10 * X + 5 * X^2 = 0'),
                    DEGREE.format(2),
                    D_ZERO,
                    '-1',
                ]
            },
            {
                'input': '5 * X^0 + 4 * X^1 = 4 * X^0',
                'messages': [
                    REDUCED.format('1 + 4 * X = 0'),
                    DEGREE.format(1),
                    D_NONE,
                    '-0.25',
                ]
            },
            {
                'input': '5 * X^0 = 4 * X^0 + 7 * X^1',
                'messages': [
                    REDUCED.format('1 - 7 * X = 0'),
                    DEGREE.format(1),
                    D_NONE,
                    '0.14285',
                ]
            },
            {
                'input': '8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0',
                'messages': [
                    REDUCED.format('5 - 6 * X - 5.6 * X^3 = 0'),
                    DEGREE.format(3),
                    BIG_DEGREE,
                ]
            },
            {
                'input': '5 * X^0 = 5 * X^0',
                'messages': [
                    REDUCED.format('0 = 0'),
                    DEGREE.format(0),
                    ALL_NUMBERS,
                ]
            },
            {
                'input': '4 * X^0 = 8 * X^0',
                'messages': [
                    REDUCED.format('-4 = 0'),
                    DEGREE.format(0),
                    NO_SOLUTION,
                ]
            },
            # {
            #     'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
            #     'messages': [
            #         REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
            #         DEGREE.format(2),
            #         D_POSITIVE,
            #         '0.90523',
            #         '-0.47513',
            #     ]
            # },
            # {
            #     'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
            #     'messages': [
            #         REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
            #         DEGREE.format(2),
            #         D_POSITIVE,
            #         '0.90523',
            #         '-0.47513',
            #     ]
            # },
            # {
            #     'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
            #     'messages': [
            #         REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
            #         DEGREE.format(2),
            #         D_POSITIVE,
            #         '0.90523',
            #         '-0.47513',
            #     ]
            # },
            # {
            #     'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
            #     'messages': [
            #         REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
            #         DEGREE.format(2),
            #         D_POSITIVE,
            #         '0.90523',
            #         '-0.47513',
            #     ]
            # },
            # {
            #     'input': '5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0',
            #     'messages': [
            #         REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
            #         DEGREE.format(2),
            #         D_POSITIVE,
            #         '0.90523',
            #         '-0.47513',
            #     ]
            # },
        ]

        for case in cases:
            print('\n' + case['input'])
            output = compute(case['input'])

            for message in case['messages']:
                with self.subTest(case['input']):
                    self.assertIn(message, output)


if __name__ == '__main__':
    unittest.main()
