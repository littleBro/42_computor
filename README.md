Computor
========

A simple yet powerful mathematics expressions interpreter made for the 42 software engineering school.

Computor_v1
-----------

Prepare: 
```
# Install python if necessary, the required version is 3.6+
brew install python

pip3 install virtualenv
virtualenv venv
```

Launch: 
```
# Activate virtualenv
source venv/bin/activate

# With an argument
./computor_v1.py "x^2 = 4"

# Interactive mode
./computor_v1.py
```

Tests: `./tests.py`

Bonuses:
- natural form input
- natural form output
- input error management
- parentheses handling: `(2 + 3) * x ^ (1+1) = 0`
- division operator: `2/3 * x = x^2 / 10`
- products and powers of polynomials: `(x + 5)^2 + (x - 5)^2 = 0`

Parsing
-------

The Computor uses the [Top Down Operator Precedence](https://en.wikipedia.org/wiki/Pratt_parser) parsing algorithm, also called Pratt parser.


It associates semantics with tokens instead of grammar rules, and uses a simple “binding power” mechanism to handle precedence levels. Traditional recursive-descent parsing is then used to handle odd or irregular portions of the syntax.

[Top Down Operator Precedence](https://tdop.github.io/) by Vaughan R. Pratt (1973)

[Top Down Operator Precedence](https://crockford.com/javascript/tdop/tdop.html) by Douglas Crockford (2007)

[Simple Top-Down Parsing in Python](http://effbot.org/zone/simple-top-down-parsing.htm) by Fredrik Lundh (2008)
