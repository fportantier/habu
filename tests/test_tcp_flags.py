import json

from click.testing import CliRunner

from habu.cli.cmd_tcp_flags import cmd_tcp_flags


def test_tcp_flags():
    runner = CliRunner()
    result = runner.invoke(cmd_tcp_flags, ['--first', '-f', 'S', '-r', 'SA', '172.217.172.228'])
    assert '-> SA' in result.output

