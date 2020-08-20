#!/usr/bin/env python3

import ipaddress
import json
import socket
import ssl

import click
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import NameOID


def cert_get_names(cert_data):

    try:
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    except ValueError:
        pass

    try:
        cert = x509.load_der_x509_certificate(cert_data, default_backend())
    except ValueError:
        raise ValueError("Not recognized cert format. Allowed: PEM or DER")

    names = set()
    names.add(cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value.lower())

    try:
        alt_names = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    except x509.extensions.ExtensionNotFound:
        alt_names = []

    if alt_names:
        for alt_name in alt_names.value.get_values_for_type(x509.DNSName):
            names.add(alt_name.lower())

    return list(sorted(names))


@click.command()
@click.option('-p', 'ports', default='443', help='Ports to connect to (comma separated list)')
@click.option('-i', 'infile', type=click.File('r'), default='-', help='Input file (Default: stdin)')
@click.option('-t', 'timeout', type=click.FLOAT, default=1, help='Time to wait for each connection')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('--json', 'json_output', is_flag=True, default=False, help='Print the output in JSON format')
@click.argument('network', default=None, required=False)
def cmd_cert_names(infile, ports, timeout, verbose, network, json_output):
    """
    Connects to each host/port and shows a summary of the certificate names.

    The hosts to connect to are taken from two possible options:

    1. -i option (default: stdin). A file where each line is a host or network

    2. An argument that can be a host or network

    If you use both methods, the hosts and networks are merged into one list.

    Example:

    \b
    $ habu.cert.names 2.18.60.240/29
    2.18.60.241         443 i.s-microsoft.com microsoft.com privacy.microsoft.com
    2.18.60.242         443 aod-ssl.itunes.apple.com aod.itunes.apple.com aodp-ssl.itunes.apple.com
    2.18.60.243         443 *.mlb.com mlb.com
    2.18.60.244         443 [SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1056)
    2.18.60.245         443 cert2-cn-public-ubiservices.ubi.com cert2-cn-public-ws-ubiservices.ubi.com
    2.18.60.246         443 *.blog.sina.com.cn *.dmp.sina.cn

    \b
    aod.itunes.apple.com
    aodp-ssl.itunes.apple.com
    aod-ssl.itunes.apple.com
    *.blog.sina.com.cn
    cert2-cn-public-ubiservices.ubi.com
    cert2-cn-public-ws-ubiservices.ubi.com
    *.dmp.sina.cn
    i.s-microsoft.com microsoft.com
    *.mlb.com mlb.com
    privacy.microsoft.com
    """

    ports = [ int(port) for port in ports.split(',') if int(port) > 0 and int(port) <= 65535 ]

    hosts = set()

    if network:
        try:
            network = ipaddress.ip_network(network, strict=False)
        except Exception as e:
            click.echo(e, err=True)
            return False

        if len(list(network.hosts())) == 0:
            hosts |= set([ipaddress.ip_address(str(network).split('/')[0])])
        else:
            hosts |= { host for host in network.hosts() }

    if not infile.isatty():
        for network in infile.read().split('\n'):
            if network:
                try:
                    network = ipaddress.ip_network(network, strict=False)
                    hosts |= { host for host in network.hosts() }
                except Exception:
                    click.echo('Ignoring invalid host/network: {}'.format(network), err=True)
                    continue

    hosts = sorted(hosts)
    all_names = set()

    if not hosts:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
        return False

    for host in hosts:
        for port in ports:

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            try:
                with socket.create_connection((str(host), int(port)), timeout=timeout) as sock:
                    with context.wrap_socket(sock) as ssock:
                        cert = ssock.getpeercert(binary_form=True)
                        names = cert_get_names(cert)
                        all_names |= set(names)
            except Exception as e:
                print(e)

    if json_output:
        print(json.dumps(sorted(all_names), indent=4))
    else:
        print('\n'.join(sorted(all_names)))


if __name__ == '__main__':
    cmd_cert_names()
