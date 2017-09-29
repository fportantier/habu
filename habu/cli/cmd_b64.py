import click
import base64
#import codecs


@click.command()
@click.argument('f', type=click.File('r'))
@click.option('-d', 'do_decode', is_flag=True, default=False, help='decode instead of encode')
def cmd_b64(f, do_decode):

    data = f.read()

    if not data:
        print("Empty file or string!")
        return 1

    #decoded = codecs.decode(data, "hex")

    if do_decode:
        print(base64.b64decode(data).decode())
    else:
        print(base64.b64encode(data.encode()).decode())


if __name__ == '__main__':
    cmd_b64()

