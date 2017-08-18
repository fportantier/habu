import click

help_text = [
    ('habu.arpoison', 'ARP cache poisoner *'),
    ('habu.arpsniff', 'ARP sniffer *'),
    ('habu.contest', 'Check internet connection capabilities'),
    ('habu.eicar', 'Print EICAR antimalware test data'),
    ('habu.forkbomb', 'Show various forkbomb examples'),
    ('habu.hasher', 'Calculate hashes using various algorithms'),
    ('habu.help', 'Print this help message'),
    ('habu.ip', 'Show your public IP'),
    ('habu.update', 'Update data files'),
    ('habu.xor', 'XOR cipher'),

]

@click.command()
def cmd_help():
    """Habu help"""

    print('* = Need root privileges')

    for c, h in help_text:
        print('%-20s%-12s' % (c, h))

if __name__ == '__main__':
    cmd_help()

