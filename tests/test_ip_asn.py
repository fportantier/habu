import json

from click.testing import CliRunner

from habu.cli.cmd_ip_asn import cmd_ip_asn


"""
{
    "asn": "15169",
    "net": "8.8.8.0/24",
    "cc": "US",
    "rir": "ARIN",
    "asname": "GOOGLE, US"
}
"""

def test_whois_ip_asn_json():
    runner = CliRunner()
    result = runner.invoke(cmd_ip_asn, ['8.8.8.8'])
    data = json.loads(result.output)
    assert data['asn'] == '15169'
    assert data['net'] == '8.8.8.0/24'
    assert data['cc'] == 'US'
    assert data['rir'] == 'ARIN'
    assert data['asname'] == 'GOOGLE, US'

