import json
import logging
import os.path
import sys
from pathlib import Path
from pprint import pprint
import magic
import click
import regex as re
import requests
import requests_cache
from bs4 import BeautifulSoup
import socket
import asyncore
import asyncio

class NClient(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = bytes('', 'ascii') #'HEAD / HTTP/1.0\r\n\r\n', 'ascii')

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]



class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


@click.command()
@click.argument('infile', type=click.File('rb'), default='-')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
@click.option('-C', 'crlf', is_flag=True, default=False, help='Use CRLF instead of LF')
def cmd_nc(infile, verbose, crlf):

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    HOST = 'www.google.com'
    PORT = 80

    loop = asyncio.get_event_loop()
    message = 'Hello World!'
    coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                                  'www.google.com', 80)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    cmd_nc()

