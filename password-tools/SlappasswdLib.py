#!/usr/bin/python
__author__ = 'sdouglas'


import hashlib
import os
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode


def hash_pass(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest() + salt)


def crack_hash(password, hash_digest):
    hash_bytes = decode(hash_digest[6:])
    digest = hash_bytes[:20]
    salt = hash_bytes[20:]
    hr = hashlib.sha1(password)
    hr.update(salt)
    return digest == hr.digest()
