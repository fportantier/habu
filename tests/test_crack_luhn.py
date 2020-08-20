import json
from time import sleep

from click.testing import CliRunner

from habu.cli.cmd_crack_luhn import cmd_crack_luhn

expected = '''4509000831606445
4509180831606445
4509260831606445
4509340831606445
4509420831606445
4509590831606445
4509670831606445
4509750831606445
4509830831606445
4509910831606445
'''

def test_crack_luhn():
    runner = CliRunner()
    result = runner.invoke(cmd_crack_luhn, ['4509-xx08-3160-6445'])
    assert result.output == expected
