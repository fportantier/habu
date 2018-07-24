import socket
import ssl
from pprint import pprint

#context = ssl.create_default_context()

#context = ssl.SSLContext()
#context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_1)
#context.verify_mode = ssl.CERT_REQUIRED
#context.check_hostname = True

#pprint(context.get_ciphers())

'''
 {'aead': False,
  'alg_bits': 128,
  'auth': 'auth-rsa',
  'description': 'CAMELLIA128-SHA         SSLv3 Kx=RSA      Au=RSA  '
                 'Enc=Camellia(128) Mac=SHA1',
  'digest': 'sha1',
  'id': 50331713,
  'kea': 'kx-rsa',
  'name': 'CAMELLIA128-SHA',
  'protocol': 'SSLv3',
  'strength_bits': 128,
  'symmetric': 'camellia-128-cbc'}]
'''

ciphers = ssl.SSLContext().get_ciphers()

for cipher in ciphers:

    #if cipher['protocol'] != 'TLSv1.2':
    #    continue

    context = ssl.SSLContext()
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    #context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_1)
    context.set_ciphers(cipher['name'])

    try:
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname="www.securetia.com")
        conn.connect(("www.securetia.com", 443))
        print(cipher['description'])
    except Exception:
        pass
        #print(cipher['name'], 'ERROR')

#cert = conn.getpeercert()


