import json
import operator

def pwdlyze(passwords):

    prefixes = {}
    postfixes = {}
    lengths = {}
    symbols = {}
    numbers = {}

    for password in passwords:

        if not password:
            continue

        prefix = password[0]
        postfix = password[-1]
        length = len(password)

        if prefix not in prefixes:
            prefixes[prefix] = 0

        prefixes[prefix] += 1

        if postfix not in postfixes:
            postfixes[postfix] = 0

        postfixes[postfix] += 1

        if length not in lengths:
            lengths[length] = 0

        lengths[length] += 1

    return {
        'prefixes' : sorted(prefixes.items(), key=operator.itemgetter(1), reverse=True)[:20],
        'postfixes' : sorted(postfixes.items(), key=operator.itemgetter(1), reverse=True)[:20],
        'lengths' : sorted(lengths.items(), key=operator.itemgetter(1), reverse=True)[:20],
    }


if __name__ == '__main__':
    with open('/home/f/code/SecLists/Passwords/darkc0de.txt', encoding='utf-8', errors='ignore') as pwdfile:
        passwords = pwdfile.read().split('\n')

    print(json.dumps(pwdlyze(passwords), indent=4))

