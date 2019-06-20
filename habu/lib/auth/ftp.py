
from habu.lib.auth.base import BaseAuth, ReturnCode
from ftplib import FTP, FTP_TLS, error_perm, Error as FTP_Error
import socket
import logging


auth_failed_messages = [
    '530 Authentication failed.',
    '530 Login authentication failed',
    '530 Login incorrect.',
    '530 Login incorrect - invalid email address',
    '530 Login or password incorrect!',
    '530 User cannot log in.',
]


class FTPAuth(BaseAuth):

    services = [ 'ftp' ]

    def login(self):

        ftp = FTP()

        try:
            ftp.connect(host=self.address, port=self.port, timeout=3)
        except socket.timeout:
            return ReturnCode.CONN_TIMEOUT
        except ConnectionRefusedError:
            return ReturnCode.CONN_REFUSED

        try:
            ftp.login(user=self.username, passwd=self.password)
            return ReturnCode.AUTH_OK
        except error_perm as e:
            if str(e) in auth_failed_messages:
                return ReturnCode.AUTH_FAILED
            else:
                return ReturnCode.GENERIC_ERROR
        except Exception:
            return ReturnCode.GENERIC_ERROR


if __name__ == '__main__':
    f = FTPAuth(username='anonymous', password='habu', address='150.101.135.3')
    print(f.login())

