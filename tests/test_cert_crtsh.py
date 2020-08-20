import json
from time import sleep

from click.testing import CliRunner

from habu.cli.cmd_cert_crtsh import cmd_cert_crtsh


def test_cert_crtsh():
    runner = CliRunner()
    result = runner.invoke(cmd_cert_crtsh, ['securetia.com'])
    assert 'www.securetia.com' in result.output

