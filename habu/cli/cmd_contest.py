import click
from habu.lib import contest


@click.command()
def cmd_contest():
    """Example script."""
    print("IP:   %s" % contest.check_ip())
    print("DNS:  %s" % contest.check_dns())
    print("FTP: %s" % contest.check_ftp())
    print("HTTP: %s" % contest.check_http())
    print("HTTPS: %s" % contest.check_https())
