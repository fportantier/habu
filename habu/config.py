import os
from pathlib import Path

#FILEDIR = os.path.dirname(os.path.abspath(__file__))
FILEDIR = Path(os.path.dirname(os.path.abspath(__file__)))
#DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
DATADIR = Path(FILEDIR / 'data') #os.path.abspath(os.path.join(FILEDIR, '../data'))
workspace = '/tmp/habu-workspace'

SERVICES_FILE_TCP = os.path.abspath(os.path.join(DATADIR, 'services-tcp'))
SERVICES_FILE_UDP = os.path.abspath(os.path.join(DATADIR, 'services-udp'))

config = {
    'FILEDIR' : Path(os.path.dirname(os.path.abspath(__file__))),
    'DATADIR' : Path(FILEDIR / 'data'),
}



if __name__ == '__main__':
    print(FILEDIR)
    print(DATADIR)
    print(config)


