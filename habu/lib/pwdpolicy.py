import click
import json
import operator

def pwdpolicy(passwords, minlength=0, need_lower=0, need_upper=0, need_number=0, need_special=0, need_families=0):

    valid = []

    for password in passwords:

        if not password:
            continue

        if len(password) < minlength:
            continue

        password = password.decode(errors='ignore')

        are_lower = 0
        are_upper = 0
        are_number = 0
        are_special = 0

        families = 0

        for ch in password:

            #print(str(ch))
            #ch = ch.decode()

            if ch.islower():
                are_lower += 1
                if are_lower == 1:
                    families += 1
                continue

            if ch.isupper():
                are_upper += 1
                if are_upper == 1:
                    families += 1
                continue

            if ch.isnumeric():
                are_number += 1
                if are_number == 1:
                    families += 1
                continue

            are_special += 1
            if are_special == 1:
                families += 1

            print(
                'lower:', are_lower,
                'upper:', are_upper,
                'number:', are_number,
                'special:', are_special,
                'families:', families
            )

        if need_families > families:
            continue

        if need_lower > are_lower:
            continue

        if need_upper > are_upper:
            continue

        if need_special > are_special:
            continue

        valid.append(password)

    return valid


@click.command()
@click.argument('infile', type=click.File('rb', errors='ignore'), default='-')
@click.option('--length', 'minlength', default=0)
@click.option('--number', 'need_number', default=0)
@click.option('--lower', 'need_lower', default=0)
@click.option('--upper', 'need_upper', default=0)
@click.option('--special', 'need_special', default=0)
@click.option('--families', 'need_families', default=0)
def cmd_pwd_policy(infile, minlength, need_number, need_lower, need_upper, need_special, need_families):

    passwords = infile.read().split(b'\n')

    valid = pwdpolicy(passwords, minlength=minlength, need_number=need_number, need_lower=need_lower, need_upper=need_upper, need_special=need_special, need_families=need_families)

    print('\n'.join(valid))

if __name__ == '__main__':
    #with open('/home/f/code/SecLists/Passwords/darkc0de.txt', encoding='utf-8', errors='ignore') as pwdfile:
    #    passwords = pwdfile.read().split('\n')

    #print(json.dumps(pwdlyze(passwords), indent=4))


    cmd_pwd_policy()


