import json
from time import sleep

from click.testing import CliRunner

from habu.cli.cmd_whois_domain import cmd_whois_domain


def test_whois_domain_json():
    sleep(1)
    runner = CliRunner()
    result = runner.invoke(cmd_whois_domain, ['google.com', '--json'])
    data = json.loads(result.output)
    assert data['org'] == 'Google LLC'


def test_whois_domain_txt():
    sleep(1)
    runner = CliRunner()
    result = runner.invoke(cmd_whois_domain, ['google.com'])
    assert 'Google LLC' in result.output
