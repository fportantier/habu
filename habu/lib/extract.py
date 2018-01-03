import re
import regex

re_email = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                       "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                       "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

re_ipv4 = re.compile(("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                      "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"))


def get_ipv4(text):
    return [email[0] for email in re.findall(re_email, text)]


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

    print(text)

    rx = r'[0-9]{13,19}'
    m = regex.findall(rx, text, overlapped=True)
    print('Before luhn', len(m))
    valid = []
    for possible in m:
        if check_luhn(possible):
            valid.append(possible)
    print('After luhn', len(valid))
    return valid




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

    print(credit_card(text))


