import json

from click.testing import CliRunner

from habu.cli.cmd_whois_ip import cmd_whois_ip


def test_whois_ip_json():
    runner = CliRunner()
    result = runner.invoke(cmd_whois_ip, ['8.8.8.8', '--json'])
    data = json.loads(result.output)
    assert data['asn_description'] == 'GOOGLE, US'


def test_whois_ip_txt():
    runner = CliRunner()
    result = runner.invoke(cmd_whois_ip, ['8.8.8.8'])
    assert 'GOOGLE, US' in result.output
