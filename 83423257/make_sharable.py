# coding=utf-8
###
# AUTHORS: CHRISTIAN GIBSON,
# PROJECT: EULER CHALLENGES
# UPDATED: JULY 24, 2015
# USAGE:   ./make_sharable keyfile.json
# EXPECTS: python 2.7.7
###

from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import json
import os


_DEFAULT_DECRYPTED_NAME = u'⁂.py'
_DEFAULT_ENCRYPTED_NAME = u'⁂.aes'

def encrypt_with_keyfile(keyfile):
    with open(keyfile, 'rb') as fh:
        keys = json.loads(fh.read())
    for directory, key in keys.items():
        encrypt_file('/'.join([directory, _DEFAULT_DECRYPTED_NAME]), handle(key))

def encrypt_file(filename, key, outname=_DEFAULT_ENCRYPTED_NAME):
    with open(filename, 'rb') as fh:
        decrypted_text = fh.read()
    encrypted_text = encrypt(decrypted_text, key)
    with open('/'.join([os.path.dirname(filename), outname]), 'wb') as fh:
        fh.write(encrypted_text)

def encrypt(decrypted_text, key):
    text = pad(decrypted_text)
    AES_IV = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, AES_IV)
    return AES_IV + cipher.encrypt(text)

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

def pad(text):
    return text + b'\0' * (AES.block_size - len(text) % AES.block_size)

if __name__ == '__main__':
    encrypt_with_keyfile('keyfile.json')
