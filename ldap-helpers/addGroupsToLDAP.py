#!/usr/bin/python
__author__ = 'Sean Douglas'
import os, sys


def check_if_root():
    user_id = os.getuid()
    if user_id != 0:
        print "This script must be run as root!"
        sys.exit(1)


def fqdn_parse(hostname):
    hostname_split = hostname.split(".")
    ldap_hostname = ""
    for i in range(len(hostname_split)):
        if i == len(hostname_split) - 1:
            ldap_hostname = ldap_hostname + "dc=" + hostname_split[i]
        else:
            ldap_hostname = ldap_hostname + "dc=" + hostname_split[i] + ","
    return ldap_hostname


def unique_members(uid_string, fqdn):
    uid_list = uid_string.split(",")
    unique_member_list = []
    for user in uid_list:
        member_str = "uniqueMember: uid=%s,ou=people,dc=opensso,%s" % (user, fqdn)
        unique_member_list.append(member_str)
    return unique_member_list


def write_ldif_file(member_list, group_name, fqdn):
    with open(group_name + "_group.ldif", "w") as f:
        dn_string = "dn: cn=%s,ou=groups,dc=opensso,%s" % (group_name, fqdn)
        f.write(dn_string+"\nobjectClass: groupOfUniqueNames\ncn: " + group_name+"\n")
        for item in member_list:
            f.write(item+"\n")


def add_groups(file_name, password, fqdn):
    command = "ldapadd -x -D 'cn=amadmin,ou=people,dc=opensso,%s' -w '%s' -f %s" % (fqdn, password, file_name)
    os.popen(command)
    print command


def main():
    check_if_root()
    print "\nEnter the unique user ids you wish to add to ROLE_USER"
    print "Example:\n\n   jsmith,bbarker,rwilliams,scolbert\n"
    user_ids = raw_input("uid(s): ")
    print "\nWhat is your hostname?"
    print "Example:\n\n   my.c2s2.local\n"
    host_name = raw_input("fqdn: ")
    print "\nEnter your openldap password."
    password = raw_input("password: ")
    ldap_formatted_fqdn = fqdn_parse(host_name)
    unique_member_list = unique_members(user_ids, ldap_formatted_fqdn)
    write_ldif_file(unique_member_list, "ROLE_USER", ldap_formatted_fqdn)
    add_groups("ROLE_USER_group.ldif", password, ldap_formatted_fqdn)
    print "\nEnter users to add to the group 'ROLE_ADMIN' separated by commas.\nExample:\n"
    users = user_ids.split(',')
    user_string = ""
    for i in range(len(users)):
        if i == len(users) - 1:
            user_string = "%s%s" % (user_string, users[i])
        else:
            user_string = "%s%s," % (user_string, users[i])
    print "   " + user_string
    print "\nNote: only select a user from the example list above."
    admin_users = raw_input("uid(s): ")
    unique_admin_list = unique_members(admin_users, ldap_formatted_fqdn)
    write_ldif_file(unique_admin_list, "ROLE_ADMIN", ldap_formatted_fqdn)
    add_groups("ROLE_ADMIN_group.ldif", password, ldap_formatted_fqdn)

if __name__ == '__main__':
    main()
