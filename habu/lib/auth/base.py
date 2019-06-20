
from enum import IntEnum


class ReturnCode(IntEnum):
    AUTH_OK = 0
    AUTH_FAILED = 1
    ACCT_BLOCKED = 2
    CONN_TIMEOUT = 3
    CONN_REFUSED = 4
    TLS_ERROR = 5
    GENERIC_ERROR = 6


class BaseAuth():

    def __init__(self, username, password, service, address, port, hostname=None, **kwargs):

        self.username = username
        self.password = password
        self.service = service
        self.address = address
        self.port = port

        if kwargs:
            self.kwargs = kwargs
            print(self.kwargs)
        else:
            self.kwargs = {}
        pass


if __name__ == '__main__':
    auth = BaseAuth('fabian', '123456', '130.89.148.12', uno=1, dos='dos', tres=None)

