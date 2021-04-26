#!/usr/bin/env python3

import ipaddress
import json
import logging

import click


def operator_gt(item, field, value):
    return field in item and float(item[field]) > float(value)

def operator_ge(item, field, value):
    return field in item and float(item[field]) >= float(value)

def operator_lt(item, field, value):
    return field in item and float(item[field]) < float(value)

def operator_le(item, field, value):
    return field in item and float(item[field]) >= float(value)

def operator_eq(item, field, value):
    return field in item and str(item[field]) == str(value)

def operator_ne(item, field, value):
    return field in item and str(item[field]) != str(value)

def operator_in_network(value1, value2):
    net1 = ipaddress.ip_network(value1)
    net2 = ipaddress.ip_network(value2)
    return net1.prefixlen >= net2.prefixlen and net2.overlaps(net1)

def operator_contains_network(value1, value2):
    net1 = ipaddress.ip_network(value1)
    net2 = ipaddress.ip_network(value2)
    return net1.prefixlen <= net2.prefixlen and net1.overlaps(net2)

def operator_in(item, field, value):

    if field not in item:
        return False

    try:
        ipaddress.ip_network(item[field])
        ipaddress.ip_network(value)
        return operator_in_network(item[field], value)
    except ValueError:
        pass

    values = value.split(',')
    return field in item and item[field] in values

def operator_contains(item, field, value):

    if field not in item:
        return False

    try:
        ipaddress.ip_network(item[field])
        ipaddress.ip_network(value)
        return operator_contains_network(item[field], value)
    except ValueError:
        pass

    return field in item and value in item[field]

def operator_defined(item, field, value):
    return field in item

def operator_undefined(item, field, value):
    return field not in item

def operator_true(item, field, value):
    return field in item and item[field] is True

def operator_false(item, field, value):
    return field in item and item[field] is False


operators = {
    'gt': operator_gt,
    'lt': operator_lt,
    'eq': operator_eq,
    'ne': operator_ne,
    'ge': operator_ge,
    'le': operator_le,
    'in': operator_in,
    'contains': operator_contains,
    'defined': operator_defined,
    'undefined': operator_undefined,
    'true': operator_true,
    'false': operator_false,
}

def operate(item, field, operator, value):
    return operators[operator](item, field, value)


@click.command()
@click.option('-i', 'infile', type=click.File('r'), default='-', help='Input file (Default: stdin)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--not', 'negated', is_flag=True, default=False, help='Negate the comparison')
@click.argument('field', type=click.STRING)
@click.argument('operator', type=click.Choice(operators.keys()))
@click.argument('value', default=None, required=False)
def cmd_data_filter(infile, verbose, negated, field, operator, value):
    """Filter data based on operators.

    Operator Reference:

    \b
    gt:         Greater than
    lt:         Lesser than
    eq:         Equal to
    ne:         Not equal to
    ge:         Greather or equal than
    le:         Lesser or equal than
    in:         Inside the list of values (or inside the network)
    contains:   Contains the value (or the network address)
    defined:    The value is defined
    undefined:  The value is not defined
    true:       The value is True
    false:      The value is False

    Example:

    \b
    $ cat /var/log/auth.log | habu.data.extract.ipv4 | habu.data.enrich | habu.data.filter cc eq US
    [
        {
            "item": "8.8.8.8",
            "family": "ipv4_address",
            "asn": "15169",
            "net": "8.8.8.0/24",
            "cc": "US",
            "rir": "ARIN",
            "asname": "GOOGLE - Google LLC, US"
        }
    ]

    \b
    Docs: https://fportantier.github.io/hacking-with-habu/user/data-manipulation.html#data-enrichment
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    if value is None and operator not in ['defined', 'undefined', 'true', 'false']:
        click.echo('Operator {} requires a value'.format(operator), err=True)

    try:
        data = json.loads(infile.read())
    except ValueError as e:
        print(e)
        click.echo('Invalid input data. Whe expect JSON here.', err=True)
        return False

    result = []

    for item in data:

        try:
            r = operate(item, field, operator, value)
        except Exception as e:
            click.echo(e, err=True)
            continue

        if r or (negated and not r):
            result.append(item)

    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    cmd_data_filter()
