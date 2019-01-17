#!/usr/bin/python
#
# ScanNetworkForSMB.py - Script for scanning network for open SMB/CIFS services
# Copyright (C) 2012 Michael Teo <miketeo (a) miketeo.net>
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the author be held liable for any damages arising from the
# use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#
# 3. This notice cannot be removed or altered from any source distribution.
#

import sys, select, socket, random, string, time
from nmb import base


class NonBlockingNetBIOS(base.NBNS):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.pendings = set()
        self.pending_count = 0

    def write(self, data, ip, port):
        assert self.sock, 'Socket is already closed'
        self.sock.sendto(data, ( ip, port ))

    def queryIPForName(self, ip):
        assert self.sock, 'Socket is already closed'

        trn_id = random.randint(1, 0xFFFF)
        data = self.prepareNetNameQuery(trn_id)
        self.write(data, ip, 137)
        self.pendings.add(ip)
        self.pending_count += 1

    def queryResult(self, ip, results):
        results = filter(lambda s: s and s[0] in string.printable, results)
        if results:
            print ip.rjust(16), '-->', ' '.join(results)

    def poll(self, timeout = 0):
        end_time = time.time() + timeout
        while self.pending_count > 0 and (timeout == 0 or time.time() < end_time):
            t = max(0, end_time - time.time())
            try:
                ready, _, _ = select.select([ self.sock.fileno() ], [ ], [ ], t)
                if not ready:
                    return None

                data, ( ip, port ) = self.sock.recvfrom(0xFFFF)
                _, ret = self.decodeIPQueryPacket(data)

                try:
                    self.pendings.remove(ip)
                    self.pending_count -= 1

                    self.queryResult(ip, set(ret))
                except KeyError: pass
            except select.error, ex:
                if type(ex) is types.TupleType:
                    if ex[0] != errno.EINTR and ex[0] != errno.EAGAIN:
                        raise ex
                else:
                    raise ex


# Originally from http://snipplr.com/view/14807/
def DottedIPToInt(dotted_ip):
    exp = 3
    intip = 0
    for quad in dotted_ip.split('.'):
        intip = intip + (int(quad) * (256 ** exp))
        exp = exp - 1
    return(intip)

def IntToDottedIP( intip ):
    octet = ''
    for exp in [3,2,1,0]:
        octet = octet + str(intip / ( 256 ** exp )) + "."
        intip = intip % ( 256 ** exp )
    return(octet.rstrip('.'))

def main():
    if len(sys.argv) > 2:
        start_ip = DottedIPToInt(sys.argv[1])
        end_ip = DottedIPToInt(sys.argv[2])
    elif len(sys.argv) == 2:
        start_ip = DottedIPToInt(sys.argv[1])
        end_ip = start_ip
    else:
        print 'ScanNetworkForSMB - Script for scanning network for open SMB/CIFS services'
        print 'Error: missing IP arguments'
        print 'Usage:', sys.argv[0], 'start-IP-address [end-IP-address]'
        print
        return

    print 'Beginning scanning %d IP addresses...' % ( end_ip-start_ip+1, )
    print

    ns = NonBlockingNetBIOS()
    for ip in range(start_ip, end_ip + 1):
        ns.queryIPForName(IntToDottedIP(ip))
        ns.poll()

    if ns.pending_count > 0:
        ns.poll(10)
        print
        print 'Query timeout. No replies from %d IP addresses' % ns.pending_count


if __name__ == '__main__':
    main()
