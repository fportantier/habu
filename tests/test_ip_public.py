import requests

from click.testing import CliRunner

from habu.cli.cmd_ip_public import cmd_ip_public


def test_whois_ip_public():
    runner = CliRunner()
    result = runner.invoke(cmd_ip_public)
    public_ip1 = result.output.strip()
    public_ip2 = requests.get('https://ifconfig.me').content.decode()

    assert public_ip1 == public_ip2

