#!/usr/bin/env python

import unittest

from computor_v1 import symbols
from mathematics.polynomial import Polynomial
from parser.computor import Computor


DEGREE = "Polynomial degree: {}"
REDUCED = "Reduced form: {}"
D_POSITIVE = "Discriminant is strictly positive, the two solutions are:"
D_NEGATIVE = "Discriminant is strictly negative, the two solutions are:"
D_ZERO = "Discriminant is zero, the solution is:"
D_NONE = "The solution is:"
ALL_NUMBERS = "All real numbers are solutions"
NO_SOLUTION = "This equation has no solutions in our world"

ERROR_BIG_DEGREE = "The polynomial degree is strictly greater than 2, I can't solve."
ERROR_NON_NATURAL_DEGREE = "Cannot solve polynomials with non-natural degrees"


class TestComputor(unittest.TestCase):
    def setUp(self):
        self.computor = Computor(symbols=symbols)

    def compute(self, s):
        self.computor.run(s, interactive=False)
        if isinstance(self.computor.result, Polynomial):
            return self.computor.result.solution_text
        return str(self.computor.result)

    def run_tests(self, tests):
        for test in tests:
            print(f"\n\n{test['input']}")
            output = self.compute(test['input'])

            for message in test['messages']:
                with self.subTest(test['input']):
                    self.assertIn(message, output)

    # Normal cases

    def test_d_positive(self):
        tests = [
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
        ]
        self.run_tests(tests)

    def test_d_negative(self):
        tests = [
            {
                'input': '5 * X^0 + 3 * X^1 + 3 * X^2 = 1 * X^0 + 0 * X^1',
                'messages': [
                    REDUCED.format('4 + 3 * X + 3 * X^2 = 0'),
                    DEGREE.format(2),
                    D_NEGATIVE,
                    '-0.5 + 1.04083i',
                    '-0.5 - 1.04083i',
                ]
            },
        ]
        self.run_tests(tests)

    def test_d_zero(self):
        tests = [
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
                'input': 'X^2 = 0',
                'messages': [
                    REDUCED.format('X^2 = 0'),
                    DEGREE.format(2),
                    D_ZERO,
                    '0',
                ]
            },
        ]
        self.run_tests(tests)

    def test_degree_1(self):
        tests = [
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
        ]
        self.run_tests(tests)

    def test_degree_big(self):
        tests = [
            {
                'input': '8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0',
                'messages': [
                    REDUCED.format('5 - 6 * X - 5.6 * X^3 = 0'),
                    DEGREE.format(3),
                    ERROR_BIG_DEGREE,
                ]
            },
        ]
        self.run_tests(tests)

    def test_degree_0(self):
        tests = [
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
        ]
        self.run_tests(tests)

    def test_parentheses(self):
        tests = [
            {
                'input': '1 - 2 * (5 * X^1 - 3 * X^2) = 10 + -3 * (X^1 + X^2)',
                'messages': [
                    REDUCED.format('-9 - 7 * X + 9 * X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '1.46184',
                    '-0.6840',
                ]
            },
            {
                'input': '1 - 2 * (5 * X^(49 - 48) - 3 * X^(1 + 1)) = 10 + -3 * (X^1 + X^2)',
                'messages': [
                    REDUCED.format('-9 - 7 * X + 9 * X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '1.46184',
                    '-0.6840',
                ]
            },
        ]
        self.run_tests(tests)

    def test_variable_case(self):
        tests = [
            {
                'input': '5 * x^0 + 3 * X^1 + 3 * x^2 = 1 * X^0 + 0 * x^1',
                'messages': [
                    REDUCED.format('4 + 3 * x + 3 * x^2 = 0'),
                    DEGREE.format(2),
                    D_NEGATIVE,
                    '-0.5 + 1.04083i',
                    '-0.5 - 1.04083i',
                ]
            },
        ]
        self.run_tests(tests)

    def test_variable_product(self):
        tests = [
            {
                'input': '5 * X^0 + 4 * X^1 - 9.3 * X * X = 1 * X^0',
                'messages': [
                    REDUCED.format('4 + 4 * X - 9.3 * X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '0.90523',
                    '-0.47513',
                ]
            },
            {
                'input': '(2 + X) * (3 + X) = 0',
                'messages': [
                    REDUCED.format('6 + 5 * X + X^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '-2',
                    '-3',
                ]
            },
        ]
        self.run_tests(tests)

    def test_rational_degree(self):
        tests = [
            {
                'input': 'x ^ 1.3 = 25 + x ^ 2',
                'messages': [
                    REDUCED.format('-25 + x^1.3 - x^2 = 0'),
                    DEGREE.format(2),
                    ERROR_NON_NATURAL_DEGREE,
                ]
            },
        ]
        self.run_tests(tests)

    def test_negative_degree(self):
        tests = [
            {
                'input': 'x ^ -1 = 25 + x ^ 2',
                'messages': [
                    REDUCED.format('-25 + x^-1 - x^2 = 0'),
                    DEGREE.format(2),
                    ERROR_NON_NATURAL_DEGREE,
                ]
            },
        ]
        self.run_tests(tests)

    def test_variable_division(self):
        tests = [
            {
                'input': 'x/x=1',
                'messages': [
                    REDUCED.format('0 = 0'),
                    DEGREE.format(0),
                    'All real numbers are solutions, except x=0',
                ]
            },
            {
                'input': '2/3 * x = x^2 / 10',
                'messages': [
                    REDUCED.format('0.666667 * x - 0.1 * x^2 = 0'),
                    DEGREE.format(2),
                    D_POSITIVE,
                    '1.11111',
                    '5.55556',
                ]
            },
        ]
        self.run_tests(tests)

    def test_powers(self):
        tests = [
            {
                'input': '(x + 5)^2 + (x - 5)^2 = 0',
                'messages': [
                    REDUCED.format('50 + 2 * x^2 = 0'),
                    DEGREE.format(2),
                    D_NEGATIVE,
                    '5i',
                    '-5i',
                ]
            },
        ]
        self.run_tests(tests)

    # Mathematical nonsense

    def test_zero_division(self):
        tests = [
            {
                'input': '0 ^ -1 = -0 ^ -0.3',
                'messages': [
                    'None',
                ]
            },
        ]
        self.run_tests(tests)

    # Incorrect input

    def test_incorrect_input(self):
        tests = [
            {
                'input': 'x^2 = 0;',
                'messages': [
                    'None',
                ]
            },
            {
                'input': '45 gbd gb',
                'messages': [
                    'None',
                ]
            },
        ]
        self.run_tests(tests)


if __name__ == '__main__':
    unittest.main()
