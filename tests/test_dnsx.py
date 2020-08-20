from habu.lib import dnsx

def test_mx():
    assert 'aspmx.l.google.com.' in dnsx.mx('google.com')

def test_ns():
    assert 'ns1.google.com.' in dnsx.ns('google.com')

def test_axfr_fail():
    assert not dnsx.axfr('google.com')

def test_axfr_success():
    assert dnsx.axfr('zonetransfer.me')

