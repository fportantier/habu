import json
from time import sleep

from click.testing import CliRunner

from habu.cli.cmd_crypto_fernet import cmd_crypto_fernet


def test_crypto_fernet_success():

    plain = 'Laiwieng9xuphahkieMohqueton3uaqu'

    runner = CliRunner()
    result1 = runner.invoke(cmd_crypto_fernet, ['-k', 'zzqNwPL_8XGPHii0vgGrWpMEi2jehGKXrDhMjL1NpDQ='], input=plain)
    encrypted = result1.output

    result2 = runner.invoke(cmd_crypto_fernet, ['-d', '-k', 'zzqNwPL_8XGPHii0vgGrWpMEi2jehGKXrDhMjL1NpDQ='], input=encrypted)
    decrypted = result2.output

    assert plain == decrypted


def test_crypto_fernet_fail():

    plain = 'Laiwieng9xuphahkieMohqueton3uaqu'

    runner = CliRunner()
    result1 = runner.invoke(cmd_crypto_fernet, ['-k', 'zzqNwPL_8XGPHii0vgGrWpMEi2jehGKXrDhMjL1NpDQ='], input=plain)
    encrypted = result1.output

    result2 = runner.invoke(cmd_crypto_fernet, ['-d', '-k', 'pCtx-U-oBmnPlZ_dXa2LSAiCYxbuPNE87x81-AC41QM='], input=encrypted)
    decrypted = result2.output

    assert plain != decrypted


