import re

re_email = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                       "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                       "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

re_ipv4 = re.compile(("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
                      "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"))


def get_ipv4(text):
    return [email[0] for email in re.findall(re_email, text)]

if __name__ == '__main__':

    text = """


    """



    print(get_ipv4('asdlasdl vllasdlas dlasdl as l  aaa@aa.com'))

