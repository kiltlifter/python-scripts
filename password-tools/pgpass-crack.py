#!/usr/bin/python
__author__ = 'sdouglas'


import PGPassLib
import optparse
import os


def process_input(user, password, pg_hash):
    pg = PGPassLib.PGPassLib()
    if os.path.isfile(user) and os.path.isfile(password):
        print pg.crack_password(user, password, pg_hash)
    elif os.path.isfile(user) or os.path.isfile(password):
        if os.path.isfile(user):
            with open(user, 'r') as users:
                password = password.split(',')
                print pg.crack_password_ambiguous(users, password, pg_hash)
        else:
            with open(password, 'r') as passwords:
                user = user.split(',')
                print pg.crack_password_ambiguous(user, passwords, pg_hash)
    else:
        user = user.split(',')
        password = password.split(',')
        print pg.crack_password_ambiguous(user, password, pg_hash)


def main():
    parser = optparse.OptionParser("pgpass-crack.py -u <user(s)> -p <password(s) -m <md5 hash>")
    parser.add_option('-u', dest='userArg', type='string', help='enter a username or file with users.')
    parser.add_option('-p', dest='passwordArg', type='string', help='enter a password or file with passwords.')
    parser.add_option('-m', dest='hashArg', type='string', help='enter a postgres md5 hash.')
    (options, args) = parser.parse_args()
    if (options.userArg is None) or (options.passwordArg is None) or (options.hashArg is None):
        print parser.usage
        exit()
    process_input(options.userArg, options.passwordArg, options.hashArg)


if __name__ == '__main__':
    main()
