#!/usr/bin/python
__author__ = 'sdouglas'


import hashlib
import os
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode


def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest() + salt)


def checkPassword(challenge_password, password):
    challenge_bytes = decode(challenge_password[6:])
    digest = challenge_bytes[:20]
    salt = challenge_bytes[20:]
    hr = hashlib.sha1(password)
    hr.update(salt)
    return digest == hr.digest()


def main():
    user_input = raw_input("Enter password: ")
    output = makeSecret(user_input)
    print output
    print checkPassword(output, user_input)


if __name__ == '__main__':
    main()
