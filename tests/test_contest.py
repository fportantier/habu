from habu.lib import contest

def test_dns_success():
    assert contest.check_dns() == True

def test_dns_fail():
    assert contest.check_dns(hostnames=['nonexistent.securetia.com']) == False

def test_http_success():
    assert contest.check_http() == True

def test_http_fail():
    assert contest.check_http(urls=['http://www.google.com:92']) == False

def test_https_success():
    assert contest.check_https() == True

def test_https_fail():
    assert contest.check_https(urls=['https://www.google.com:92']) == False

def test_ftp_success():
    assert contest.check_ftp() == True

def test_ftp_fail():
    assert contest.check_ftp(servers=['nonexistent.securetia.com']) == False

def test_ssh_success():
    assert contest.check_ssh() == True

def test_ssh_fail():
    assert contest.check_ssh(servers=['www.google.com']) == False


