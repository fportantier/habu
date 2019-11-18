#!/usr/bin/env python3

import dns.resolver
import dns.zone


def resolve(name, server=None):
    """resolves the name"""

    my_resolver = dns.resolver.Resolver()

    if server:
        my_resolver.nameservers = [server]

    result = []

    try:
        answers = my_resolver.query(str(name), lifetime=3)
    except Exception as e:
        answers = []

    answers = [ str(answer) for answer in answers ]

    return answers




def ns(domain):
    """returns a list with the NS servers for domain"""

    result = []

    try:
        answers = dns.resolver.query(domain, 'NS')
    except Exception:
        answers = []

    #if not answers:
    #    answers = []

    for rdata in answers:
        result.append(str(rdata.target).lower())

    return result


def mx(domain):
    """returns a list with the MX servers for domain"""

    result = []

    try:
        answers = dns.resolver.query(domain, 'MX')
    except Exception:
        answers = []

    #if not answers:
    #    answers = []

    for rdata in answers:
        result.append(str(rdata.exchange).lower())

    return result


def axfr(domain):
    """ returns a list with the ns that allows zone transfers"""

    allowed = []

    for server in ns(domain):

        try:
            z = dns.zone.from_xfr(dns.query.xfr(server, domain))
            if z.nodes.keys():
                allowed.append(server)
        except Exception as e:
            pass

    return allowed


if __name__ == '__main__':
    print(ns('securetia.com'))
    print(mx('securetia.com'))
    print(axfr('securetia.com'))

