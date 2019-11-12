import regex
import validators


def check_luhn(cc):

    sum = 0
    parity = len(cc) % 2

    for i, digit in enumerate([int(x) for x in cc]):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum += digit

    return sum % 10 == 0


def credit_card(text):

    rx = r'[0-9]{13,19}'
    m = regex.findall(rx, text, overlapped=True)
    #print('Before luhn', len(m))
    valid = []
    for possible in m:
        if check_luhn(possible):
            valid.append(possible)
    #print('After luhn', len(valid))
    return valid



validator_functions = {
    'ipv4_address' : validators.ipv4,
    'ipv4_network' : validators.ipv4_cidr,
    'ipv6_address' : validators.ipv6,
    'ipv6_network' : validators.ipv6_cidr,
    'domain' : validators.domain,
    'email' : validators.email,
    'url' : validators.url,
    'mac_address' : validators.mac_address,
    'md5' : validators.md5,
    'sha1' : validators.sha1,
    'sha224' : validators.sha224,
    'sha256' : validators.sha256,
    'sha512' : validators.sha512,
    'pan' : credit_card,
}


def guess_item_type(item):
    for item_type, function in validator_functions.items():
        if function(item):
            return item_type
    return None


if __name__ == '__main__':

    text = """
    VISA:
    4024007141679679
    4929838390718057
    4556789306248228608
    MasterCard:
    5425016886151184
    2221005662102894
    5535224890915019
    American Express (AMEX):
    341200896841032
    349764688249508
    372421022345415
    Discover:
    6011793427332832
    6011260018752893
    6011679156694765000
    JCB:
    3528351232225189
    3544543527236778
    3533678501612139597
    Diners Club - North America:
    5456878950482775
    5524961995313599
    5547678103880250
    Diners Club - Carte Blanche:
    30225940317115
    30473596040272
    30272074894170
    Diners Club - International:
    36682688303216
    36705742855069
    36622473207743
    Maestro:
    6759336225624384
    6763077648725655
    5020380847601144
    Visa Electron:
    4508018645020067
    4913484711396667
    4913987879409494
    InstaPayment:
    6390379018975931
    6380946373456228
    6387276287896233
    """

    #print(credit_card(text))

    test_items = [
        '8.8.4.4',
        'www.google.com',
        'google.com',
        'https://www.google.com',
        'xxss://www.google.com',
        '60b725f10c9c85c70d97880dfe8191b3',
        '3f786850e387550fdab836ed7e6dc881de23001b',
        '7c297c1793fdad2ac52a68bdd6b8fde3eb59b99c3f8c44710fde5fd7',
        '87428fc522803d31065e7bce3cf03fe475096631e5e07bbd7a0fde60c4cf25c7',
        '162b0b32f02482d5aca0a7c93dd03ceac3acd7e410a5f18f3fb990fc958ae0df6f32233b91831eaf99ca581a8c4ddf9c8ba315ac482db6d4ea01cc7884a635be',
        'test@asd.com',
        '@æ|nothingforhere!',
        '4913484711396667',
    ]

    for item in test_items:
        print(item, guess_item_type(item))
