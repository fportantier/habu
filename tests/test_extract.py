from habu.lib.extract import guess_item_type

def test_ipv4_address():
    assert guess_item_type('8.8.8.8') == 'ipv4_address'

def test_ipv4_network():
    assert guess_item_type('8.8.8.0/24') == 'ipv4_network'

def test_ipv6_address():
    assert guess_item_type('2001:0db8:85a3:0000:0000:8a2e:0370:7334') == 'ipv6_address'

def test_ipv6_network():
    assert guess_item_type('2001:db8:1234::/48') == 'ipv6_network'

def test_url():
    assert guess_item_type('https://www.securetia.com') == 'url'

def test_domain():
    assert guess_item_type('securetia.com') == 'domain'

def test_md5():
    assert guess_item_type('60b725f10c9c85c70d97880dfe8191b3') == 'md5'

def test_sha1():
    assert guess_item_type('3f786850e387550fdab836ed7e6dc881de23001b') == 'sha1'

def test_sha224():
    assert guess_item_type('7c297c1793fdad2ac52a68bdd6b8fde3eb59b99c3f8c44710fde5fd7') == 'sha224'

def test_sha256():
    assert guess_item_type('87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0fde60c4cf25c7') == 'sha256'

def test_sha512():
    assert guess_item_type('162b0b32f02482d5aca0a7c93dd03ceac3acd7e410a5f18f3fb990fc958ae0df6f32233b91831eaf99ca581a8c4ddf9c8ba315ac482db6d4ea01cc7884a635be') == 'sha512'

def test_email():
    assert guess_item_type('awesome@securetia.com') == 'email'

def test_pan():
    assert guess_item_type('4913484711396667') == 'pan'

