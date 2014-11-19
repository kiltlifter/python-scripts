#!/usr/bin/python
import os
import sys
import getpass
import time
import subprocess


def check_if_root():
    uid = os.getuid()
    if uid != 0:
        print "Please run this script as root!"
        sys.exit(1)


def find_dc(domain_name):
    domain_list = domain_name.split(".")
    combo_string = ""
    for i in range(len(domain_list)):
        if i < len(domain_list) - 1:
            combo_string = combo_string + "dc=" + domain_list[i] + ","
        else:
            combo_string = combo_string + "dc=" + domain_list[i]
    return combo_string


def password_hash(passwd):
    slapd_command = "slappasswd -s %s" % (passwd)
    hashed_pass = os.popen(slapd_command, "r")
    temp_hash = hashed_pass.read()
    return temp_hash.rstrip("\r\n")


def add_olcRootPW(pass_hash, input_file):
    olcRootPW_command = "echo 'olcRootPW: %s' >> %s" % (pass_hash, input_file)
    os.popen(olcRootPW_command)


def add_olcSuffix(input_file, domain_components):
    olcSuffix_command = "sed -i 's/olcSuffix.*/olcSuffix: %s/' %s" % (domain_components, input_file)
    os.popen(olcSuffix_command)


def add_olcRootDN(input_file, domain_components):
    olcRootDN_command = "sed -i 's/olcRootDN.*/olcRootDN: cn=Manager,%s/' %s" % (domain_components, input_file)
    os.popen(olcRootDN_command)


def add_olcAccess(input_file):
    olcAccess_command = "echo -n 'olcAccess: to * by * write' >> %s" % (input_file)
    os.popen(olcAccess_command)


def restart_slapd():
    os.popen("/etc/init.d/slapd restart")


def restart_tomcat():
    os.popen("/etc/init.d/tomcat7 restart")


def configure_openam_user_store(fqdn, amadmin_password):
    domain_components = find_dc(fqdn)
    command = "echo -e '%s\n%s\n%s' | " % (domain_components, fqdn, amadmin_password) + \
              "/usr/share/doc/openldap-servers-2.4.23/configure_openam_user_store.sh"
    os.popen(command)


def check_if_passwords_match(pass1, pass2):
    if pass1 == pass2:
        return pass1
    else:
        print "Passwords don't match."
        sys.exit()


def domain_name_prompt():
    probable_hostname = os.uname()[1]
    yes_no = raw_input("Is this your Fully Qualified Domain Name?\n" + probable_hostname + " [Y/n]: ")
    if yes_no == ("Y" or "y"):
        return probable_hostname
    else:
        provided_hostname = raw_input("Domain Name: ")
        return provided_hostname


def execute_commands(fqdn, ldap_password, amadmin_password):
    bdb_ldif = "/etc/openldap/slapd.d/cn=config/olcDatabase={2}bdb.ldif"
    config_ldif = "/etc/openldap/slapd.d/cn=config/olcDatabase={0}config.ldif"
    # Find the Domain Components in the provided FQDN
    domain_components = find_dc(fqdn)
    # Hash the provided password with slappasswd
    hashed_password = password_hash(ldap_password)
    # Add the olcRootPW directive to the provided files
    print "Editing LDAP config files."
    add_olcRootPW(hashed_password, bdb_ldif)
    add_olcRootPW(hashed_password, config_ldif)
    # Add the olcSuffix directive to the provided file
    add_olcSuffix(bdb_ldif, domain_components)
    # Add the olcRootDN directive to the provided file
    add_olcRootDN(bdb_ldif, domain_components)
    # Add the olcAccess directive to the provided file
    add_olcAccess(bdb_ldif)
    # Restart the ldap service
    print "Restarting the LDAP service."
    restart_slapd()
    time.sleep(5)
    configure_openam_user_store(fqdn, amadmin_password)


def main():
    check_if_root()
    fqdn = domain_name_prompt()
    ldap_password1 = getpass.getpass("Create a LDAP password (acceptable characters are [A-Za-z0-9./]): ")
    ldap_password2 = getpass.getpass("Enter one more time: ")
    ldap_password = check_if_passwords_match(ldap_password1, ldap_password2)
    amadmin_password1 = getpass.getpass("Create an amadmin password (acceptable characters are [A-Za-z0-9./]): ")
    amadmin_password2 = getpass.getpass("Enter one more time: ")
    amadmin_password = check_if_passwords_match(amadmin_password1, amadmin_password2)
    execute_commands(fqdn, ldap_password, amadmin_password)


if __name__ == '__main__':
    main()
