# coding=utf-8
###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: EULER CHALLENGES
# UPDATED: JULY 24, 2015
# USAGE:   ./make_readable keyfile.json
# EXPECTS: python 2.7.7
###

from Crypto.Cipher import AES
import hashlib
import json
import os


_DEFAULT_DECRYPTED_NAME = u'⁂.py_d'
_DEFAULT_ENCRYPTED_NAME = u'⁂.aes'

def decrypt_with_keyfile(keyfile):
    with open(keyfile, 'rb') as fh:
        keys = json.loads(fh.read())
    for directory, key in keys.items():
        decrypt_file('/'.join([directory, _DEFAULT_ENCRYPTED_NAME]), handle(key))

def decrypt_file(filename, key, outname=_DEFAULT_DECRYPTED_NAME):
    with open(filename, 'rb') as fh:
        encrypted_text = fh.read()
    decrypted_text = decrypt(encrypted_text, key)
    with open('/'.join([os.path.dirname(filename), outname]), 'wb') as fh:
        fh.write(decrypted_text)

def decrypt(encrypted_text, key):
    AES_IV = encrypted_text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, AES_IV)
    decrypted_text = cipher.decrypt(encrypted_text[AES.block_size:])
    return decrypted_text.rstrip(b'\0')

def handle(key, key_length=32, method=lambda k : hashlib.sha256(k).digest()):
    key_bytes = bytearray()

    try:
        key_bytes.extend(method(key))
    except:
        key_bytes.extend(method(key.encode('utf-8')))

    if len(key_bytes) <= key_length:
        while len(key_bytes) < key_length:
            key_bytes.append(key_bytes[((key_length - len(key_bytes))
                                        % len(key_bytes) - 1)])
    else:
        key_bytes = key_bytes[:key_length]

    return str(key_bytes)

if __name__ == '__main__':
    decrypt_with_keyfile('keyfile.json')
