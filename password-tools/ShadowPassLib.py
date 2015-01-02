#!/usr/bin/python
__author__ = 'sdouglas'


import crypt
from random import SystemRandom as _SystemRandom
import string as _string


class ShadowPassLib():
    def __init__(self):
        self.character_set = _string.ascii_letters + _string.digits + "./"

    def __create_salt(self, length):
        random_obj = _SystemRandom()
        salt_list = random_obj.sample(self.character_set, length)
        return "".join(salt_list)

    def create_hash(self, hash_type, salt_len, password):
        salt = "$%s$%s" % (hash_type, self.__create_salt(salt_len))
        return crypt.crypt(password, salt)

    @staticmethod
    def decrypt_hash(shadow_hash, password):
        hash_split = shadow_hash.split("$")
        salt = "$" + hash_split[1] + "$" + hash_split[2]
        new_hash = crypt.crypt(password, salt)
        if new_hash == shadow_hash:
            return password
        else:
            return None

