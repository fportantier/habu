import click

from habu.lib import contest


@click.command()
def cmd_contest():
    """Example script."""
    print("IP:    %s" % contest.check_ip())
    print("DNS:   %s" % contest.check_dns())
    print("FTP:   %s" % contest.check_ftp())
    #print("SSH:   %s" % contest.check_ssh())
    print("HTTP:  %s" % contest.check_http())
    print("HTTPS: %s" % contest.check_https())


if __name__ == '__main__':
    cmd_contest()
