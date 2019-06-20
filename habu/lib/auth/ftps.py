
from habu.lib.auth.base import BaseAuth, ReturnCode
from ftplib import FTP, FTP_TLS, error_perm, Error as FTP_Error
import socket
import logging

class FTPSAuth(BaseAuth):

    services = [ 'ftps' ]

    def login(self):

        if self.service == 'ftp':
            ftp = FTP()
        else:
            #print('doing FTP SSL')
            ftp = FTP_TLS()

        try:
            ftp.connect(host=self.address, port=self.port, timeout=3)
        except socket.timeout:
            return ReturnCode.CONN_TIMEOUT

        if self.service == 'ftps':
            logging.info('Securing SSL/TLS connection...')
            print('Securing SSL/TLS connection...')
            try:
                print(ftp.auth())
                print(ftp.prot_p())
                #print(ftp.prot_p())
            except error_perm as e:
                logging.info(e) #'Error during SSL/TLS setup.')
                print(e)
                #if str(e).startswith('500'):
                    #logging.info('Maybe the server doesn\'t supports FTPS')
                return ReturnCode.TLS_ERROR

        try:
            #print(self.service)
            #ftp.connect(host=self.address, port=self.port, timeout=3)
            #if self.service == 'ftps':
            ftp.login(user=self.username, passwd=self.password)
            return ReturnCode.AUTH_OK
        except ConnectionRefusedError:
            return ReturnCode.CONN_REFUSED
        except error_perm as e:
            print(e)
            return ReturnCode.AUTH_FAILED
        except Exception:
            return ReturnCode.GENERIC_ERROR


if __name__ == '__main__':
    f = FTPAuth(username='anonymous', password='habu', address='150.101.135.3')
    print(f.login())

