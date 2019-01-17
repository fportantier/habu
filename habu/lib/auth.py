

import ftplib

class AuthBase():

    def __init__(self, **kwargs):
        print(kwargs)

    def authenticate(self):
        return True


class FTP(AuthBase):

    def authenticate(self):
        with ftplib.FTP(host="ftp1.at.proftpd.org") as ftp:
            try:
                ftp.login(user="anonymous", passwd="auth")
                return True
            except ftplib.error_perm:
                return False


class SMB(AuthBase):

    def authenticate(self):

        from smb.SMBConnection import SMBConnection

        # There will be some mechanism to capture userID, password, client_machine_name, server_name and server_ip
        # client_machine_name can be an arbitary ASCII string
        # server_name should match the remote machine name, or else the connection will be rejected

        #userID = 'xatportantier'
        userID = 'guest'
        #password = 'SecurFMP_23'
        password = ''
        client_machine_name = 'fmp'
        server_ip = '192.1.3.120'
        server_name = 'Server72'
        server_name = ''

        from nmb.NetBIOS import NetBIOS

        nb = NetBIOS(broadcast=True, listen_port=0)
        #print('ip', nb.queryName(server_name, port=445))
        #print('name', nb.queryIPForName(server_ip))


        conn = SMBConnection(userID, password, client_machine_name, server_name, use_ntlm_v2=True, is_direct_tcp=False)
        from pprint import pprint
        for a in [ 'capabilities', 'domain', 'host_type', 'log', 'my_name', 'remote_name', 'security_mode', 'uid', 'username' ]:
            print(a, getattr(conn, a))
        #print('cap', conn.capabilities)
        #print('domain', conn.domain)

        print('auth', conn.connect(server_ip, 139))
        #print(conn.isUsingSMB2)
        #print(conn.echo('aaaaa'))
        #conn.listShares()

if __name__ == '__main__':
    auth = SMB()
    print(auth.authenticate())


'''
 'auth_result',
 'capabilities',
 'close',
 'connect',
 'connected_trees',
 'createDirectory',
 'data_buf',
 'data_nmb',
 'deleteDirectory',
 'deleteFiles',
 'domain',
 'echo',
 'feedData',
 'getAttributes',
 'has_authenticated',
 'has_negotiated',
 'host_type',
 'isUsingSMB2',
 'is_busy',
 'is_direct_tcp',
 'is_signing_active',
 'is_using_smb2',
 'listPath',
 'listShares',
 'listSnapshots',
 'log',
 'max_buffer_size',
 'max_mpx_count',
 'max_raw_size',
 'max_read_size',
 'max_transact_size',
 'max_write_size',
 'mid',
 'my_name',
 'next_rpc_call_id',
 'next_signing_id',
 'onAuthFailed',
 'onAuthOK',
 'onNMBSessionFailed',
 'onNMBSessionMessage',
 'onNMBSessionOK',
 'password',
 'pending_requests',
 'remote_name',
 'rename',
 'requestNMBSession',
 'resetFileAttributes',
 'retrieveFile',
 'retrieveFileFromOffset',
 'security_mode',
 'sendNMBMessage',
 'sendNMBPacket',
 'session_id',
 'sign_options',
 'signing_challenge_response',
 'signing_session_key',
 'smb_message',
 'sock',
 'storeFile',
 'storeFileFromOffset',
 'uid',
 'use_ntlm_v2',
 'use_plaintext_authentication',
 'username',
 'write']
'''
