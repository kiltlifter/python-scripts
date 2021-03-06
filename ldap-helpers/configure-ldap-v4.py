#!/usr/bin/python
import os
import getpass
import time
import hashlib
import os
from base64 import urlsafe_b64encode as encode
from subprocess import *


def check_if_root():
    uid = os.getuid()
    if uid != 0:
        print "Please run this script as root!"
        exit()


def find_dc(domain_name):
    domain_list = domain_name.split(".")
    combo_string = ""
    for i in range(len(domain_list)):
        if i < len(domain_list) - 1:
            combo_string = combo_string + "dc=" + domain_list[i] + ","
        else:
            combo_string = combo_string + "dc=" + domain_list[i]
    return combo_string


#def password_hash(password):
#    salt = os.urandom(4)
#    h = hashlib.sha1(str(password))
#    h.update(salt)
#    return "{SSHA}" + encode(h.digest() + salt)


def password_hash(password):
    hash_command = "slappasswd -s %s" % password
    slapd_pass = Popen(hash_command, shell=True, stdout=PIPE).stdout.read()
    return slapd_pass.rstrip("\n")

def add_olcRootPW(pass_hash, input_file):
    olcRootPW_command = "echo 'olcRootPW: %s' >> %s" % (pass_hash, input_file)
    Popen(olcRootPW_command, shell=True, stdout=PIPE).stdout.read()


def add_olcSuffix(input_file, domain_components):
    olcSuffix_command = "sed -i 's/olcSuffix.*/olcSuffix: %s/' %s" % (domain_components, input_file)
    Popen(olcSuffix_command, shell=True, stdout=PIPE).stdout.read()


def add_olcRootDN(input_file, domain_components):
    olcRootDN_command = "sed -i 's/olcRootDN.*/olcRootDN: cn=Manager,%s/' %s" % (domain_components, input_file)
    Popen(olcRootDN_command, shell=True, stdout=PIPE).stdout.read()


def add_olcAccess(input_file):
    olcAccess_command = "echo -n 'olcAccess: to * by * write' >> %s" % input_file
    Popen(olcAccess_command, shell=True, stdout=PIPE).stdout.read()


def restart_slapd():
    Popen("/etc/init.d/slapd restart", shell=True, stdout=PIPE).stdout.read()


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


def write_file(data, name):
    with open(name, "w") as f:
        f.write(data)


def openam_user_store(fqdn, amadmin_pass, ldap_pass):
    domain_components = find_dc(fqdn)
    dom_dot = fqdn.split(".")[0]
    amadmin_hash = password_hash(amadmin_pass)

    user_store = "dn: cn=openam,cn=schema,cn=config\n" + \
        "objectClass: olcSchemaConfig\n" + \
        "cn: openam\n" + \
        "olcAttributeTypes: {0}( 2.16.840.1.113730.3.1.1072 NAME 'iplanet-am-user-admin-start-dn' DESC 'Starting DN for Admin User' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {1}( 1.3.6.1.4.1.42.2.27.9.1.63 NAME 'iplanet-am-auth-login-success-url' DESC 'Redirection URL After Successful Login' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {2}( 1.3.6.1.4.1.1466.101.120.43 NAME 'preferredTimeZone' DESC 'preferred time zone for a person' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE X-ORIGIN 'iPlanet' )\n" + \
        "olcAttributeTypes: {3}( 1.3.6.1.4.1.42.2.27.9.1.839 NAME 'sunIdentityServerPPLegalIdentityVATIdValue' DESC 'Liberty PP IDValue' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {4}( 1.3.6.1.4.1.36733.2.2.1.118 NAME ( 'coreTokenInteger03' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {5}( 2.16.840.1.113730.3.1.1071 NAME 'iplanet-am-user-auth-modules' DESC 'User Auth Modules' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {6}( 1.3.6.1.4.1.42.2.27.9.1.65 NAME 'iplanet-am-auth-post-login-process-class' DESC 'Class Name for Post Authentication Processing' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {7}( 1.3.6.1.4.1.36733.2.2.1.3.1 NAME ( 'assignedDashboard' ) DESC 'Dashboard App registry' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenAM' )\n" + \
        "olcAttributeTypes: {8}( 1.3.6.1.4.1.36733.2.2.1.117 NAME ( 'coreTokenInteger02' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {9}( 1.3.6.1.4.1.36733.2.2.1.4 NAME 'devicePrintProfiles' DESC 'Device print profiles information is stored in this attribute' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenAM' )\n" + \
        "olcAttributeTypes: {10}( 1.3.6.1.4.1.36733.2.2.1.98 NAME ( 'coreTokenExpirationDate' ) DESC 'Token expiration date' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {11}( 1.3.6.1.4.1.42.2.27.9.1.823 NAME 'sunIdentityMSISDNNumber' DESC 'User MSISDN Number' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {12}( 2.16.840.1.113730.3.1.976 NAME 'iplanet-am-user-account-life' DESC 'User Account Life' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {13}( 1.3.6.1.4.1.36733.2.2.1.108 NAME ( 'coreTokenString08' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {14}( 1.3.6.1.4.1.42.2.27.9.1.853 NAME 'sunIdentityServerPPFacadeGreetSound' DESC 'Liberty PP FacadeGreetSound' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {15}( 1.3.6.1.4.1.36733.2.2.1.109 NAME ( 'coreTokenString09' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {16}( 1.3.6.1.4.1.36733.2.2.1.125 NAME ( 'coreTokenInteger10' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {17}( 1.3.6.1.4.1.36733.2.2.1.119 NAME ( 'coreTokenInteger04' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {18}( 1.3.6.1.4.1.42.2.27.9.1.828 NAME 'sunIdentityServerPPCommonNameMN' DESC 'Liberty PP CommonName MN' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {19}( 1.3.6.1.4.1.42.2.27.9.1.862 NAME 'sunIdentityServerPPEmergencyContact' DESC 'Liberty PP EmergencyContact' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {20}( 1.3.6.1.4.1.36733.2.2.1.99 NAME ( 'coreTokenUserId' ) DESC 'ID of the owning user' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {21}( 1.3.6.1.4.1.42.2.27.9.1.856 NAME 'sunIdentityServerPPDemographicsLanguage' DESC 'Liberty PP DemographicsLanguage' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {22}( 1.3.6.1.4.1.36733.2.2.1.104 NAME ( 'coreTokenString04' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {23}( 2.16.840.1.113730.3.1.1053 NAME 'iplanet-am-session-service-status' DESC 'Session Service Status' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {24}( 1.3.6.1.4.1.42.2.27.9.1.860 NAME 'sunIdentityServerPPSignKey' DESC 'Liberty PP SignKey' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {25}( 1.3.6.1.4.1.36733.2.2.1.105 NAME ( 'coreTokenString05' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {26}( 1.3.6.1.4.1.42.2.27.9.1.82 NAME ( 'sunPluginSchema' ) DESC 'To store the plugin schema information' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {27}( 1.3.6.1.4.1.36733.2.2.1.128 NAME ( 'coreTokenDate03' ) DESC 'General mapped date field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {28}( 1.3.6.1.4.1.42.2.27.9.1.59 NAME 'iplanet-am-user-alias-list' DESC 'User Alias Names List' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {29}( 1.3.6.1.4.1.42.2.27.9.1.73 NAME 'iplanet-am-user-federation-info-key' DESC 'User Federation Information Key' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {30}( 1.3.6.1.4.1.36733.2.2.1.110 NAME ( 'coreTokenString10' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {31}( 2.16.840.1.113730.3.1.692 NAME 'inetUserStatus' DESC '\"active\", \"inactive\", or \"deleted\" status of a user' EQUALITY caseIgnoreMatch SINGLE-VALUE SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'Nortel subscriber interoperability' )\n" + \
        "olcAttributeTypes: {32}( 1.3.6.1.4.1.36733.2.2.1.130 NAME ( 'coreTokenDate05' ) DESC 'General mapped date field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {33}( 1.3.6.1.4.1.36733.2.2.1.120 NAME ( 'coreTokenInteger05' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {34}( 1.3.6.1.4.1.42.2.27.9.1.58 NAME 'iplanet-am-user-auth-config' DESC 'User Authentication Configuration' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {35}( 1.3.6.1.4.1.42.2.27.9.1.81 NAME ( 'sunsmspriority' ) DESC 'To store the priority of the service with respect to its siblings' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {36}( 1.3.6.1.4.1.36733.2.2.1.101 NAME ( 'coreTokenString01' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {37}( 1.3.6.1.4.1.42.2.27.9.1.854 NAME 'sunIdentityServerPPFacadegreetmesound' DESC 'Liberty PP FacadeMeGreetSound' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {38}( 1.3.6.1.4.1.36733.2.2.1.97 NAME ( 'coreTokenType' ) DESC 'Token type' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {39}( 1.3.6.1.4.1.42.2.27.9.1.851 NAME 'sunIdentityServerPPFacadeWebSite' DESC 'Liberty PP FacadeWebSite' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {40}( 1.3.6.1.4.1.36733.2.2.1.103 NAME ( 'coreTokenString03' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {41}( 1.3.6.1.4.1.1466.101.120.42 NAME 'preferredLocale' DESC 'preferred locale for a person' EQUALITY caseIgnoreMatch SUBSTR caseIgnoreSubstringsMatch SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 SINGLE-VALUE X-ORIGIN 'iPlanet' )\n" + \
        "olcAttributeTypes: {42}( 1.3.6.1.4.1.42.2.27.9.1.832 NAME 'sunIdentityServerPPLegalIdentityLegalName' DESC 'Liberty PP LegalName' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {43}( 1.3.6.1.4.1.36733.2.2.1.116 NAME ( 'coreTokenInteger01' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {44}( 1.3.6.1.4.1.42.2.27.9.1.83 NAME ( 'sunKeyValue' ) DESC 'Attribute to store the encoded key values of the services' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {45}( 1.3.6.1.4.1.42.2.27.9.1.62 NAME 'iplanet-am-auth-configuration' DESC 'Authentication Configuration' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {46}( 1.3.6.1.4.1.42.2.27.9.1.84 NAME ( 'sunxmlKeyValue' ) DESC 'Attribute to store the key values in xml format' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {47}( 1.3.6.1.4.1.42.2.27.9.1.859 NAME 'sunIdentityServerPPDemographicsTimeZone' DESC 'Liberty PP DemographicsTimeZone' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {48}( 1.3.6.1.4.1.42.2.27.9.1.834 NAME 'sunIdentityServerPPLegalIdentityMaritalStatus' DESC 'Liberty PP Marital Status' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {49}( 1.3.6.1.4.1.42.2.27.9.1.836 NAME 'sunIdentityServerPPLegalIdentityAltIdType' DESC 'Liberty PP AltID Type' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {50}( 2.16.840.1.113730.3.1.1069 NAME 'iplanet-am-session-destroy-sessions' DESC 'Destroy Session' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {51}( 1.3.6.1.4.1.42.2.27.9.1.79 NAME ( 'sunserviceID' ) DESC 'Attribute to store the reference to the inherited object' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {52}( 1.3.6.1.4.1.36733.2.2.1.129 NAME ( 'coreTokenDate04' ) DESC 'General mapped date field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {53}( 1.3.6.1.4.1.36733.2.2.1.96 NAME ( 'coreTokenId' ) DESC 'Token unique ID' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {54}( 1.3.6.1.4.1.42.2.27.9.1.74 NAME 'iplanet-am-user-federation-info' DESC 'User Federation Information' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {55}( 1.3.6.1.4.1.42.2.27.9.1.989 NAME 'sun-fm-saml2-nameid-infokey' DESC 'SAML 2.0 Name Identifier Information Key' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {56}( 1.3.6.1.4.1.42.2.27.9.1.825 NAME 'sunIdentityServerPPCommonNameCN' DESC 'Liberty PP CommonName CN' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {57}( 1.3.6.1.4.1.36733.2.2.1.100 NAME ( 'coreTokenObject' ) DESC 'Serialised JSON object for Token' SYNTAX 1.3.6.1.4.1.1466.115.121.1.5  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {58}( 1.2.840.113556.1.2.102 NAME 'memberof' DESC 'Group that the entry belongs to' SYNTAX 1.3.6.1.4.1.1466.115.121.1.12 X-ORIGIN 'iPlanet Delegated Administrator' )\n" + \
        "olcAttributeTypes: {59}( 1.3.6.1.4.1.36733.2.2.1.102 NAME ( 'coreTokenString02' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {60}( 1.3.6.1.4.1.36733.2.2.1.115 NAME ( 'coreTokenString15' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {61}( 1.3.6.1.4.1.42.2.27.9.1.838 NAME 'sunIdentityServerPPLegalIdentityVATIdType' DESC 'Liberty PP IDType' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {62}( 1.3.6.1.4.1.42.2.27.9.1.830 NAME 'sunIdentityServerPPCommonNamePT' DESC 'Liberty PP CommonName PersonalTitle' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {63}( 1.3.6.1.4.1.42.2.27.9.1.841 NAME 'sunIdentityServerPPEmploymentIdentityOrg' DESC 'Liberty PP Org' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {64}( 1.3.6.1.4.1.42.2.27.9.1.837 NAME 'sunIdentityServerPPLegalIdentityAltIdValue' DESC 'Liberty PP AltID Type' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {65}( 1.3.6.1.4.1.42.2.27.9.1.831 NAME 'sunIdentityServerPPInformalName' DESC 'Liberty PP InformalName' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {66}( 1.3.6.1.4.1.42.2.27.9.1.591 NAME 'iplanet-am-user-password-reset-force-reset' DESC 'Password Reset Force Reset password' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {67}( 1.3.6.1.4.1.42.2.27.9.1.857 NAME 'sunIdentityServerPPDemographicsAge' DESC 'Liberty PP DemographicsAge' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {68}( 1.3.6.1.4.1.42.2.27.9.1.829 NAME 'sunIdentityServerPPCommonNameAltCN' DESC 'Liberty PP CommonName Alt CN' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {69}( 1.3.6.1.4.1.36733.2.2.1.121 NAME ( 'coreTokenInteger06' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {70}( 1.3.6.1.4.1.36733.2.2.1.123 NAME ( 'coreTokenInteger08' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {71}( 2.16.840.1.113730.3.1.1073 NAME 'iplanet-am-user-service-status' DESC 'User Service Status' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {72}( 1.3.6.1.4.1.42.2.27.9.1.858 NAME 'sunIdentityServerPPDemographicsBirthDay' DESC 'Liberty PP DemographicsBirthDay' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {73}( 1.3.6.1.4.1.42.2.27.9.1.852 NAME 'sunIdentityServerPPFacadeNamePronounced' DESC 'Liberty PP FacadeNamePronounced' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {74}( 2.16.840.1.113730.3.1.1067 NAME 'iplanet-am-session-max-caching-time' DESC 'Max Session Caching Time' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {75}( 1.3.6.1.4.1.36733.2.2.1.107 NAME ( 'coreTokenString07' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {76}( 1.3.6.1.4.1.42.2.27.9.1.835 NAME 'sunIdentityServerPPLegalIdentityGender' DESC 'Liberty PP Gender' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {77}( 1.3.6.1.4.1.42.2.27.9.1.590 NAME 'iplanet-am-user-password-reset-question-answer' DESC 'Password Reset User Question Answer' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {78}( 1.3.6.1.4.1.42.2.27.9.1.826 NAME 'sunIdentityServerPPCommonNameFN' DESC 'Liberty PP CommonName FN' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {79}( 1.3.6.1.4.1.42.2.27.9.1.855 NAME 'sunIdentityServerPPDemographicsDisplayLanguage' DESC 'Liberty PP DemographicsDisplayLanguage' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {80}( 2.16.840.1.113730.3.1.1068 NAME 'iplanet-am-session-get-valid-sessions' DESC 'Get Valid Sessions' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {81}( 1.3.6.1.4.1.36733.2.2.1.124 NAME ( 'coreTokenInteger09' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {82}( 1.3.6.1.4.1.42.2.27.9.1.78 NAME ( 'sunServiceSchema' ) DESC 'SMS Attribute to Store xml schema of a particular service' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcAttributeTypes: {83}( 1.3.6.1.4.1.36733.2.2.1.113 NAME ( 'coreTokenString13' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {84}( 1.3.6.1.4.1.42.2.27.9.1.842 NAME 'sunIdentityServerPPEmploymentIdentityAltO' DESC 'Liberty PP Alt Orgs' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {85}( 1.3.6.1.4.1.42.2.27.9.1.849 NAME 'sunIdentityServerPPMsgContact' DESC 'Liberty PP MsgContact' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {86}( 2.16.840.1.113730.3.1.1074 NAME 'iplanet-am-user-login-status' DESC 'User Login Status' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {87}( 1.3.6.1.4.1.42.2.27.9.1.821 NAME 'sunIdentityServerDiscoEntries' DESC 'User DiscoEntries' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {88}( 1.3.6.1.4.1.36733.2.2.1.122 NAME ( 'coreTokenInteger07' ) DESC 'General mapped integer field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.27  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {89}( 1.3.6.1.4.1.42.2.27.9.1.850 NAME 'sunIdentityServerPPFacadeMugShot' DESC 'Liberty PP FacadeMugShot' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {90}( 1.3.6.1.4.1.42.2.27.9.1.793 NAME 'sunAMAuthInvalidAttemptsData' DESC 'XML data for Invalid Login Attempts' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {91}( 1.3.6.1.4.1.36733.2.2.1.114 NAME ( 'coreTokenString14' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {92}( 2.16.840.1.113730.3.1.1070 NAME 'iplanet-am-session-add-session-listener-on-all-sessions' DESC 'Add Session Listener on All Sessions' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {93}( 1.3.6.1.4.1.42.2.27.9.1.827 NAME 'sunIdentityServerPPCommonNameSN' DESC 'Liberty PP CommonName SN' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {94}( 1.3.6.1.4.1.42.2.27.9.1.71 NAME 'iplanet-am-user-success-url' DESC 'Redirection URL for Successful User Authentication' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {95}( 1.3.6.1.4.1.42.2.27.9.1.72 NAME 'iplanet-am-user-failure-url' DESC 'Redirection URL for Failed User Authentication' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {96}( 1.3.6.1.4.1.42.2.27.9.1.990 NAME 'sun-fm-saml2-nameid-info' DESC 'SAML 2.0 Name Identifier Information' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {97}( 1.3.6.1.4.1.42.2.27.9.1.848 NAME 'sunIdentityServerPPAddressCard' DESC 'Liberty PP AddressCard' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {98}( 1.3.6.1.4.1.42.2.27.9.1.589 NAME 'iplanet-am-user-password-reset-options' DESC 'Password Reset Options' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {99}( 2.16.840.1.113730.3.1.1066 NAME 'iplanet-am-session-max-idle-time' DESC 'Max Session Idle Time' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {100}( 1.3.6.1.4.1.42.2.27.9.1.833 NAME 'sunIdentityServerPPLegalIdentityDOB' DESC 'Liberty PP Date of Birth' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {101}( 2.16.840.1.113730.3.1.1065 NAME 'iplanet-am-session-max-session-time' DESC 'Max Service Time' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {102}( 2.16.840.1.113730.3.1.693 NAME 'inetUserHttpURL' DESC 'A users Web addresses' SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 X-ORIGIN 'Nortel subscriber interoperability' )\n" + \
        "olcAttributeTypes: {103}( 1.3.6.1.4.1.42.2.27.9.1.861 NAME 'sunIdentityServerPPEncryptKey' DESC 'Liberty PP EncryPTKey' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {104}( 1.3.6.1.4.1.42.2.27.9.1.840 NAME 'sunIdentityServerPPEmploymentIdentityJobTitle' DESC 'Liberty PP JobTitle' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {105}( 1.3.6.1.4.1.36733.2.2.1.106 NAME ( 'coreTokenString06' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {106}( 1.3.6.1.4.1.36733.2.2.1.111 NAME ( 'coreTokenString11' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {107}( 1.3.6.1.4.1.36733.2.2.1.112 NAME ( 'coreTokenString12' ) DESC 'General mapped string field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {108}( 1.3.6.1.4.1.42.2.27.9.1.752 NAME 'iplanet-am-session-quota-limit' DESC 'Session Quota Constraints' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {109}( 1.3.6.1.4.1.42.2.27.9.1.64 NAME 'iplanet-am-auth-login-failure-url' DESC 'Redirection URL for Failed User Authentication' SYNTAX 1.3.6.1.4.1.1466.115.121.1.15 X-ORIGIN 'OpenSSO' )\n" + \
        "olcAttributeTypes: {110}( 1.3.6.1.4.1.36733.2.2.1.126 NAME ( 'coreTokenDate01' ) DESC 'General mapped date field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcAttributeTypes: {111}( 1.3.6.1.4.1.36733.2.2.1.127 NAME ( 'coreTokenDate02' ) DESC 'General mapped date field' SYNTAX 1.3.6.1.4.1.1466.115.121.1.24  SINGLE-VALUE X-ORIGIN 'ForgeRock OpenAM CTSv2' )\n" + \
        "olcObjectClasses: {0}( 1.3.6.1.4.1.36733.2.2.2.4 NAME 'devicePrintProfilesContainer' DESC 'Class containing device print profiles' SUP top AUXILIARY MAY ( devicePrintProfiles ) X-ORIGIN 'OpenAM' )\n" + \
        "olcObjectClasses: {1}( 1.3.6.1.4.1.42.2.27.9.2.25 NAME 'sunservice' DESC 'object containing service information' SUP top MUST ou MAY ( labeledURI $ sunServiceSchema $ sunKeyValue $ sunxmlKeyValue $ sunPluginSchema $ description ) X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcObjectClasses: {2}( 1.3.6.1.4.1.36733.2.2.2.3.1 NAME 'forgerock-am-dashboard-service' AUXILIARY MAY ( assignedDashboard ) X-ORIGIN 'Forgerock' )\n" + \
        "olcObjectClasses: {3}( 2.16.840.1.113730.3.2.175 NAME 'iplanet-am-session-service' DESC 'Session Service OC' SUP top AUXILIARY MAY ( iplanet-am-session-max-session-time $ iplanet-am-session-max-idle-time $ iplanet-am-session-max-caching-time $ iplanet-am-session-quota-limit $ iplanet-am-session-get-valid-sessions $ iplanet-am-session-destroy-sessions $ iplanet-am-session-add-session-listener-on-all-sessions $ iplanet-am-session-service-status ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {4}( 1.3.6.1.4.1.42.2.27.9.2.118 NAME 'sunAMAuthAccountLockout' DESC 'Invalid Login Attempts Object Class' SUP top AUXILIARY MAY ( sunAMAuthInvalidAttemptsData ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {5}( 1.3.6.1.4.1.42.2.27.9.2.27 NAME 'sunservicecomponent' DESC 'Sub-components of the service' SUP organizationalUnit MUST ou MAY ( labeledURI $ sunserviceID $ sunsmspriority $ sunKeyValue $ sunxmlKeyValue $ description ) X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcObjectClasses: {6}( 1.3.6.1.4.1.42.2.27.9.2.148 NAME 'sunFMSAML2NameIdentifier' DESC 'SAML 2.0 name identifier objectclass' SUP top AUXILIARY MAY ( sun-fm-saml2-nameid-infokey $ sun-fm-saml2-nameid-info ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {7}( 1.3.6.1.4.1.42.2.27.9.2.76 NAME 'sunFederationManagerDataStore' DESC 'FSUser provider OC' SUP top AUXILIARY MAY ( iplanet-am-user-federation-info-key $ iplanet-am-user-federation-info $ sunIdentityServerDiscoEntries) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {8}( 2.16.840.1.113730.3.2.184 NAME 'iplanet-am-managed-person' DESC 'Managed Person OC' SUP top AUXILIARY MAY ( iplanet-am-user-account-life ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {9}( 1.3.6.1.4.1.42.2.27.9.2.127 NAME 'sunIdentityServerLibertyPPService' DESC 'sunIdentityServerLibertyPPService OC' SUP top AUXILIARY MAY ( sunIdentityServerPPCommonNameCN $ sunIdentityServerPPCommonNameAltCN $ sunIdentityServerPPCommonNameFN $ sunIdentityServerPPCommonNameSN $ sunIdentityServerPPCommonNamePT $ sunIdentityServerPPCommonNameMN $ sunIdentityServerPPInformalName $ sunIdentityServerPPLegalIdentityLegalName $ sunIdentityServerPPLegalIdentityDOB $ sunIdentityServerPPLegalIdentityMaritalStatus $ sunIdentityServerPPLegalIdentityGender $ sunIdentityServerPPLegalIdentityAltIdType $ sunIdentityServerPPLegalIdentityAltIdValue $ sunIdentityServerPPLegalIdentityVATIdType $ sunIdentityServerPPLegalIdentityVATIdValue $sunIdentityServerPPEmploymentIdentityJobTitle $ sunIdentityServerPPEmploymentIdentityOrg $ sunIdentityServerPPEmploymentIdentityAltO $ sunIdentityServerPPAddressCard $ sunIdentityServerPPMsgContact $ sunIdentityServerPPFacadeMugShot $ sunIdentityServerPPFacadeWebSite $ sunIdentityServerPPFacadeNamePronounced $ sunIdentityServerPPFacadeGreetSound $ sunIdentityServerPPFacadegreetmesound $ sunIdentityServerPPDemographicsDisplayLanguage $ sunIdentityServerPPDemographicsLanguage $ sunIdentityServerPPDemographicsBirthDay $ sunIdentityServerPPDemographicsAge $ sunIdentityServerPPDemographicsTimeZone $ sunIdentityServerPPSignKey $ sunIdentityServerPPEncryptKey $ sunIdentityServerPPEmergencyContact ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {10}( 2.16.840.1.113730.3.2.176 NAME 'iplanet-am-user-service' DESC 'User Service OC' SUP top AUXILIARY MAY ( iplanet-am-user-auth-modules $ iplanet-am-user-login-status $ iplanet-am-user-admin-start-dn $ iplanet-am-user-auth-config $ iplanet-am-user-alias-list $ iplanet-am-user-success-url $ iplanet-am-user-failure-url $ iplanet-am-user-password-reset-options $ iplanet-am-user-password-reset-question-answer $ iplanet-am-user-password-reset-force-reset $ sunIdentityMSISDNNumber ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {11}( 1.3.6.1.4.1.1466.101.120.142 NAME 'iPlanetPreferences' AUXILIARY MAY ( preferredLanguage $ preferredLocale $ preferredTimeZone ) X-ORIGIN 'iPlanet' )\n" + \
        "olcObjectClasses: {12}( 1.3.6.1.4.1.42.2.27.9.2.104 NAME 'sunRealmService' DESC 'object containing service information for realms' SUP top MAY ( o $ labeledURI $ sunKeyValue $ sunxmlKeyValue $ description ) X-ORIGIN 'Sun Java System Identity Management' )\n" + \
        "olcObjectClasses: {13}( 1.3.6.1.4.1.42.2.27.9.2.23 NAME 'iplanet-am-auth-configuration-service' DESC 'Authentication Configuration Service OC' SUP top AUXILIARY MAY ( iplanet-am-auth-configuration $ iplanet-am-auth-login-success-url $ iplanet-am-auth-login-failure-url $ iplanet-am-auth-post-login-process-class ) X-ORIGIN 'OpenSSO' )\n" + \
        "olcObjectClasses: {14}( 2.16.840.1.113730.3.2.130 NAME 'inetuser' DESC 'Auxiliary class which has to be present in an entry for delivery of subscriber services' SUP top AUXILIARY MAY ( uid $ inetUserStatus $ inetUserHTTPURL $ userPassword $ memberof ) X-ORIGIN 'Nortel subscriber interoperability' )\n" + \
        "olcObjectClasses: {15}( 1.3.6.1.4.1.36733.2.2.2.27 NAME 'frCoreToken' DESC 'object containing ForgeRock Core Token' SUP top STRUCTURAL MUST ( coreTokenId $ coreTokenType ) MAY ( coreTokenExpirationDate $ coreTokenUserId $ coreTokenObject $ coreTokenString01 $ coreTokenString02 $ coreTokenString03 $ coreTokenString04 $ coreTokenString05 $ coreTokenString06 $ coreTokenString07 $ coreTokenString08 $ coreTokenString09 $ coreTokenString10 $ coreTokenString11 $ coreTokenString12 $ coreTokenString13 $ coreTokenString14 $ coreTokenString15 $ coreTokenInteger01 $ coreTokenInteger02 $ coreTokenInteger03 $ coreTokenInteger04 $ coreTokenInteger05 $ coreTokenInteger06 $ coreTokenInteger07 $ coreTokenInteger08 $ coreTokenInteger09 $ coreTokenInteger10 $ coreTokenDate01 $ coreTokenDate02 $ coreTokenDate03 $ coreTokenDate04 $ coreTokenDate05 ) X-ORIGIN 'ForgeRock OpenAM CTSv2' )"

    base_entries = "dn: %s\n" % domain_components + \
        "objectclass: dcObject\n" + \
        "objectclass: organization\n" + \
        "o: %s\n" % fqdn + \
        "dc: %s\n\n" % dom_dot + \
        "dn: dc=opensso,%s\n" % domain_components + \
        "objectClass: top\n" + \
        "objectClass: dcObject\n" + \
        "objectClass: organization\n" + \
        "o: opensso\n" + \
        "dc: opensso\n\n" + \
        "dn: ou=people,dc=opensso,%s\n" % domain_components + \
        "objectClass: top\n" + \
        "ou:people\n" + \
        "objectClass: organizationalUnit\n\n" + \
        "dn: ou=groups,dc=opensso,%s\n" % domain_components + \
        "ou:groups\n" + \
        "objectClass: top\n" + \
        "objectClass: organizationalUnit\n\n" + \
        "dn: cn=amadmin,ou=people,dc=opensso,%s\n" % domain_components + \
        "objectclass: inetuser\n" + \
        "objectclass: organizationalperson\n" + \
        "objectclass: person\n" + \
        "objectclass: top\n" + \
        "cn: amadmin\n" + \
        "sn: amadmin\n" + \
        "uid: amadmin\n" + \
        "userPassword: %s\n\n" % amadmin_hash + \
        "dn:cn=defaultGroup,ou=groups,dc=opensso,%s\n" % domain_components + \
        "objectclass: top\n" + \
        "objectclass: groupofnames\n" + \
        "member:cn=amadmin,ou=people,dc=opensso,%s\n" % domain_components + \
        "cn:default1"

    user_store_file = "openam_user_store_config.ldif"
    write_file(user_store, user_store_file)
    load_configuration = "ldapadd -x -D 'cn=config' -f %s -w '%s'" % (user_store_file, ldap_pass)
    print "Connecting to ldap as Config..."
    print Popen(load_configuration, shell=True, stdout=PIPE).stdout.read()
    os.remove(user_store_file)

    default_entries = "openam_default_entries.ldif"
    write_file(base_entries, default_entries)
    add_base_entries = "ldapadd -x -D 'cn=Manager,%s' -f %s -w " \
                       "'%s'" % (domain_components, default_entries, ldap_pass)
    print "Connecting to ldap as Manager..."
    print Popen(add_base_entries, shell=True, stdout=PIPE).stdout.read()
    os.remove(default_entries)


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
    time.sleep(2)
    openam_user_store(fqdn, amadmin_password, ldap_password)


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
