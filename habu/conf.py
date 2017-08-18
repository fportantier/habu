import os

FILEDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
workspace = '/tmp/habu-workspace'

SERVICES_FILE_TCP = os.path.abspath(os.path.join(DATADIR, 'services-tcp'))
SERVICES_FILE_UDP = os.path.abspath(os.path.join(DATADIR, 'services-udp'))


