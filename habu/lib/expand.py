from habu.lib.identify import identify
from habu.lib.ip2asn import ip2asn

expanders = {}
expanders['IPAddress'] = []
expanders['IPNetwork'] = []
expanders['Unknown'] = []
expanders['IPAddress'].append(ip2asn)


def expand(asset):

    family = identify(asset)

    result = {
        'asset': asset,
        'family' : family,
    }


    for expander in expanders[family]:
        result.update(expander(asset))



    return result


