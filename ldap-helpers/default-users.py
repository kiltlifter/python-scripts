#!/usr/bin/python
__author__ = 'sdouglas'


import getpass
import optparse
import os
from subprocess import *


user_dict = {
    'users': {
        'sdouglas': {
            'fname': 'Sean',
            'lname': 'Douglas',
            'fullname': 'Sean Douglas',
            'password': 'password'
        },
        'jadams': {
            'fname': 'James',
            'lname': 'Adams',
            'fullname': 'James Adams',
            'password': 'password'
        },
        'lfinan': {
            'fname': 'Ling',
            'lname': 'Finan',
            'fullname': 'Ling Finan',
            'password': 'password'
        },
        'rwhiteside': {
            'fname': 'Rob',
            'lname': 'Whiteside',
            'fullname': 'Rob Whiteside',
            'password': 'password'
        },
        'jfrey': {
            'fname': 'John',
            'lname': 'Frey',
            'fullname': 'John Frey',
            'password': 'password'
        },
        'wernest': {
            'fname': 'William',
            'lname': 'Ernest',
            'fullname': 'William Ernest',
            'password': 'password'
        },
        'rtobin': {
            'fname': 'Ryan',
            'lname': 'Tobin',
            'fullname': 'Ryan Tobin',
            'password': 'password'
        },
        'kshaw': {
            'fname': 'Kevin',
            'lname': 'Shaw',
            'fullname': 'Kevin Shaw',
            'password': 'password'
        },
        'bstevens': {
            'fname': 'Barbara',
            'lname': 'Stevens',
            'fullname': 'Barbara Stevens',
            'password': 'password'
        },
        'jdoe': {
            'fname': 'John',
            'lname': 'Doe',
            'fullname': 'John Doe',
            'password': 'password'
        },
        'jsnow': {
            'fname': 'Jon',
            'lname': 'Snow',
            'fullname': 'Jon Snow',
            'password': 'password'
        },

    }
}


def ldap_person_entry(fqdn, amadmin_password):
    for item in user_dict['users']:
        ldap_string = "dn: uid=%s,ou=people,dc=opensso,%s\n" % (item, fqdn) + \
            "cn: %s\n" % user_dict['users'][item]['fullname'] + \
            "givenName: %s\n" % user_dict['users'][item]['fname'] + \
            "sn: %s\n" % user_dict['users'][item]['lname'] + \
            "inetUserStatus: Active\nobjectClass: devicePrintProfilesContainer\nobjectClass: person\n" \
            "objectClass: sunIdentityServerLibertyPPService\nobjectClass: sunFederationManagerDataStore\n" \
            "objectClass: inetOrgPerson\nobjectClass: iPlanetPreferences\n" \
            "objectClass: iplanet-am-auth-configuration-service\nobjectClass: organizationalPerson\n" \
            "objectClass: sunFMSAML2NameIdentifier\nobjectClass: inetuser\n" \
            "objectClass: forgerock-am-dashboard-service\nobjectClass: iplanet-am-managed-person\n" \
            "objectClass: sunAMAuthAccountLockout\nobjectClass: iplanet-am-user-service\nobjectClass: top\n" \
            "uid: %s\n" % item + \
            "userPassword: %s" % user_dict['users'][item]['password']
        add_user_command = "echo '%s' | ldapadd -x -D 'cn=amadmin,ou=people,dc=opensso,%s'" \
                           " -w '%s'" % (ldap_string, fqdn, amadmin_password)
        Popen(add_user_command, shell=True, stdout=PIPE).stdout.read()


def find_dc(domain_name):
    domain_list = domain_name.split(".")
    combo_string = ""
    for i in range(len(domain_list)):
        if i < len(domain_list) - 1:
            combo_string = combo_string + "dc=" + domain_list[i] + ","
        else:
            combo_string = combo_string + "dc=" + domain_list[i]
    return combo_string


def main():
    parser = optparse.OptionParser("default-users.py -d <domain>")
    parser.add_option('-d', dest='hostName', type='string', help='specify a domain name')
    (options, args) = parser.parse_args()
    host_name = options.hostName
    amadmin_pass = getpass.getpass("Password for amadmin: ")
    if host_name is None:
        print parser.usage
        exit()
    ldap_person_entry(find_dc(host_name), amadmin_pass)


if __name__ == '__main__':
    main()
