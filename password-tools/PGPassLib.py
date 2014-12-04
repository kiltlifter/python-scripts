#!/usr/bin/python
__author__ = 'sdouglas'

import hashlib


class PGPassLib():
    def __init__(self):
        self.type = 'md5'

    def decrypt_md5_hash(self, username, passwd, pg_hash):
        try:
            test_hash = self.type + hashlib.md5(str(passwd)+str(username)).hexdigest()
            if test_hash == pg_hash:
                return True
        except Exception, e:
            print str(e)
        return False

    def create_md5_hash(self, username, passwd):
        try:
            pg_hash = self.type + hashlib.md5(str(passwd)+str(username)).hexdigest()
            return pg_hash
        except Exception, e:
            print str(e)
        return None

    def crack_password(self, username_file, passwd_file, pg_hash):
        try:
            with open(username_file, 'r') as usernames:
                for user in usernames:
                    with open(passwd_file, 'r') as passwords:
                        for password in passwords:
                            if self.decrypt_md5_hash(user.rstrip("\n\r"), password.rstrip("\n\r"), pg_hash):
                                return "Username: %s\nPassword: %s" % (user.rstrip("\n\r"), password.rstrip("\n\r"))
        except Exception, e:
            print str(e)
        return None

    def crack_password_ambiguous(self, user, passwd, pg_hash):
        try:
            for usr in user:
                for ps in passwd:
                    if self.decrypt_md5_hash(usr.rstrip("\n\r"), ps.rstrip("\n\r"), pg_hash):
                        return "Username: %s\nPassword: %s" % (usr.rstrip("\n\r"), ps.rstrip("\n\r"))
        except Exception, e:
            print str(e)
        return None
