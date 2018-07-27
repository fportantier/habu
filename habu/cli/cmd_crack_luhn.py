#!/usr/bin/env python3

import sys
import logging

import click


def luhn_validate(number):
    """ Source code from: https://en.wikipedia.org/wiki/Luhn_algorithm"""

    sum = 0
    parity = len(number) % 2
    for i, digit in enumerate([int(x) for x in number]):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum += digit
    return sum % 10 == 0


@click.command()
@click.argument('number')
def cmd_crack_luhn(number):
    """Having known values for a Luhn validated number, obtain the possible unknown numbers.

    Numbers that use the Luhn algorithm for validation are Credit Cards, IMEI,
    National Provider Identifier in the United States, Canadian Social
    Insurance Numbers, Israel ID Numbers and Greek Social Security Numbers (ΑΜΚΑ).

    The '-' characters are ignored.

    Define the missing numbers with the 'x' character.

    Reference: https://en.wikipedia.org/wiki/Luhn_algorithm

    Example:

    \b
    $ habu.crack.luhn 4509-xxxx-3160-6445
    """

    number = number.replace('-', '')
    unknown_count = number.count('x')

    if not number.replace('x', '').isdigit():
        print('Invalid format. Please, read the documentation.', file=sys.stderr)
        sys.exit(1)

    for n in range(10 ** unknown_count):
        candidate = number
        for item in '{:0{count}}'.format(n, count=unknown_count):
            candidate = candidate.replace('x', item, 1)
        if luhn_validate(candidate):
            print(candidate)


if __name__ == '__main__':
    cmd_crack_luhn()

