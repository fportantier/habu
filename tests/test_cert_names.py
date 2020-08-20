import json
from time import sleep

from click.testing import CliRunner

from habu.cli.cmd_cert_names import cmd_cert_names


def test_cert_names_txt():
    runner = CliRunner()
    result = runner.invoke(cmd_cert_names, ['2.18.60.241'])
    assert 'www.microsoft.com' in result.output

def test_cert_names_json():
    runner = CliRunner()
    result = runner.invoke(cmd_cert_names, ['2.18.60.241', '--json'])
    data = json.loads(result.output)
    assert 'www.microsoft.com' in data
