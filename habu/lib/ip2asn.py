
import ipaddress

import dns.resolver


def ip2asn(ipaddr):
    """Returns the ASN data associated with an IP (v4 or v6)

    >>> from pprint import pprint
    >>> pprint(ip2asn('8.8.8.8'))
    {'asn': '15169',
     'asname': 'GOOGLE - Google Inc., US',
     'cc': 'US',
     'net': '8.8.8.0/24',
     'rir': 'ARIN'}
    >>> pprint(ip2asn('2001:4860:4860::8888'))
    {'asn': '15169',
     'asname': 'GOOGLE - Google Inc., US',
     'cc': 'US',
     'net': '2001:4860::/32',
     'rir': 'ARIN'}
    >>> pprint(ip2asn('unk'))
    None
    """

    try:
        ip = ipaddress.ip_network(ipaddr)
    except ValueError:
        return None

    if ip.is_private:
        return None

    if ip.version == 4:

        a, b, c, d = str(ip.exploded).split('/')[0].split('.')
        reversed = "%s.%s.%s.%s" % (d, c, b, a)
        name = "%s.origin.asn.cymru.com" % (reversed)

    else:
        only_addr = str(ip.exploded).split('/')[0].replace(':', '')

        reversed = ''

        for number in only_addr[::-1]:

            reversed += number
            reversed += '.'

        reversed = reversed.rstrip('.')

        name = "%s.origin6.asn.cymru.com" % (reversed)

    try:
        response = dns.resolver.query(name, 'TXT')
    except:
        return None

    # "15169 | 8.8.4.0/24 | US | arin |"
    r = {}
    r['asn'] = response[0].to_text().split('|')[0].strip(" \"").split(' ')[0]
    r['net'] = response[0].to_text().split('|')[1].strip(" \"")
    r['cc'] = response[0].to_text().split('|')[2].strip(" \"")
    r['rir'] = response[0].to_text().split('|')[3].strip(" \"").upper()
    r['asname'] = 'unknown'

    # Get AS Name
    # "15169 | US | arin | 2000-03-30 | GOOGLE - Google Inc.,US"
    try:
        name = "AS%s.asn.cymru.com" % (r['asn'])
        response = dns.resolver.query(name, 'TXT')
        r['asname'] = response[0].to_text().split('|')[4].strip(" \"")
    except:
        pass

    return(r)


if __name__ == '__main__':
    print(ip2asn('8.8.8.8'))


