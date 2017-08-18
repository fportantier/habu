import os
from glob import glob

FILEDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
BOMBDIR = os.path.join(DATADIR, 'forkbomb')

bombs = [
    'bash',
    'batch',
    'c',
    'haskell',
    'perl',
    'php',
    'python',
    'ruby',
]

def get_bomb(bomb):

    if bomb not in bombs:
        return ''

    with open(BOMBDIR + '/' + bomb + '.txt') as b:
        return b.read()


if __name__ == '__main__':
    print(get_bomb('c'))

