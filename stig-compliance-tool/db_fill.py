__author__ = 'sdouglas'

# Note: this script is only intended to fill the database. Please excuse the verbosity and non-compiance to standards
# aka, the hackiness.

import sqlite3


# Update a row in the database. Parameters are the db connection and a list of 5 strings
def update_row(db_conn, stig_values):
    # Create the cursor object
    cursor = db_conn.cursor()
    # Define a list to hold our tuples
    tuple_value = []
    # Iterate through our list of strings, creating a list of tuples used as a parameter to our sql execute method.
    for val in stig_values:
        tuple_value.append((val),)
    # Update a row of data with the parameters supplied.
    cursor.execute(
        '''UPDATE stigs
        SET check_command_debian = ?, check_command_redhat = ?, fix_command_debian = ?, fix_command_redhat = ?
        WHERE id = ?''', tuple_value
    )


def stig_v_38437(connection):
    stig_id = "V-38437"
    # If any stdout is returned, we can assume autofs is present.
    check_command_debian = "/bin/grep -o autofs /etc/fstab\n" \
                           "/usr/bin/find -L /etc/rc2.d /etc/rc3.d /etc/rc4.d /etc/rc5.d -name S*autofs*"
    check_command_redhat = "/bin/grep -o autofs /etc/fstab\n" \
                           "/bin/find -L /etc/rc2.d /etc/rc3.d /etc/rc4.d /etc/rc5.d -name S*autofs*"
    # To correct the issue, stop the autofs service and disable it on all run levels.
    fix_command_debian = "/usr/sbin/service autofs stop\n" \
                         "/usr/sbin/update-rc.d autofs disable 0123456"
    fix_command_redhat = "/sbin/service autofs stop\n" \
                         "/sbin/chkconfig --level 0123456 autofs off"

    # List of strings to be ingested by the update_row function
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    # Pass our connection and list of values to the function that updates a row in the database
    update_row(connection, values)


def stig_v_38438(connection):
    stig_id = "V-38438"
    # If grep finds audit = 1 in the GRUB_CMDLINE_LINUX directive then it will be printed.
    check_command_debian = """/bin/grep -E "^GRUB_CMDLINE_LINUX=.*(audit=1|audit\s=\s1|audit =1|audit= 1)" /etc/default/grub"""
    # If grep finds audit =1 on the kernel line of /etc/grub.conf then it will be printed.
    check_command_redhat = """/bin/grep -E "kernel\s.*(audit=1|audit\s=\s1|audit =1|audit= 1)" /etc/grub.conf"""
    # Inserts audit=1 into the GRUB_CMDLINE_LINUX directive
    fix_command_debian = """/bin/sed -i 's/\(GRUB_CMDLINE_LINUX=".*\)"/\1 audit=1"/' /etc/default/grub"""
    # Inserts audit=1 on to the kernel parameter line of /etc/grub.conf
    fix_command_redhat = """/bin/sed -i 's/.*\(kernel\s.*\)/\1 audit=1/' /etc/grub.conf"""
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38448(connection):
    stig_id = "V-38448"
    # exit code should be 0, and contain the string /etc/gshadow
    check_command_debian = "/usr/bin/find /etc/gshadow -group root"
    check_command_redhat = "/bin/find /etc/gshadow -group root"
    fix_command_debian = "/bin/chgrp root /etc/gshadow"
    fix_command_redhat = "/bin/chgrp root /etc/gshadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38449(connection):
    stig_id = "V-38449"
    # exit code should be 0, and contain the string /etc/gshadow
    check_command_debian = "/usr/bin/find /etc/gshadow -perm 0000"
    check_command_redhat = "/bin/find /etc/gshadow -perm 0000"
    fix_command_debian = "/bin/chmod 0000 /etc/gshadow"
    fix_command_redhat = "/bin/chmod 0000 /etc/gshadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38450(connection):
    stig_id = "V-38450"
    # exit code should be 0, and contain the string /etc/passed
    check_command_debian = "/usr/bin/find /etc/passwd -user root"
    check_command_redhat = "/bin/find /etc/passwd -user root"
    fix_command_debian = "/bin/chown root /etc/passwd"
    fix_command_redhat = "/bin/chown root /etc/passwd"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38451(connection):
    stig_id = "V-38451"
    # exit code should be 0, and contain the string /etc/passed
    check_command_debian = "/usr/bin/find /etc/passwd -group root"
    check_command_redhat = "/bin/find /etc/passwd -group root"
    fix_command_debian = "/bin/chgrp root /etc/passwd"
    fix_command_redhat = "/bin/chgrp root /etc/passwd"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38455(connection):
    stig_id = "V-38455"
    # If anything is returned, this is a finding
    check_command_debian = """/bin/df -h /tmp | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /tmp | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38456(connection):
    stig_id = "V-38456"
    # If anything is returned, this is a finding
    check_command_debian = """/bin/df -h /var | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /var | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38457(connection):
    stig_id = "V-38457"
    # exit code should be 0, and contain the string /etc/passed
    check_command_debian = "/usr/bin/find /etc/passwd -perm 0644"
    check_command_redhat = "/bin/find /etc/passwd -perm 0644"
    fix_command_debian = "/bin/chmod 0644 /etc/passwd"
    fix_command_redhat = "/bin/chmod 0644 /etc/passwd"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38458(connection):
    stig_id = "V-38458"
    # exit code should be 0, and contain the string /etc/group
    check_command_debian = "/usr/bin/find /etc/group -user root"
    check_command_redhat = "/bin/find /etc/group -user root"
    fix_command_debian = "/bin/chown root /etc/group"
    fix_command_redhat = "/bin/chown root /etc/group"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38459(connection):
    stig_id = "V-38459"
    # exit code should be 0, and contain the string /etc/group
    check_command_debian = "/usr/bin/find /etc/group -user root"
    check_command_redhat = "/bin/find /etc/group -user root"
    fix_command_debian = "/bin/chgrp root /etc/group"
    fix_command_redhat = "/bin/chgrp root /etc/group"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38461(connection):
    stig_id = "V-38461"
    check_command_debian = "/usr/bin/find /etc/group -perm 0664"
    check_command_redhat = "/bin/find /etc/group -perm 0664"
    fix_command_debian = "/bin/chmod 0644 /etc/group"
    fix_command_redhat = "/bin/chmod 0644 /etc/group"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38463(connection):
    stig_id = "V-38463"
    # If anything is returned, then /var/log is not mounted on it's own partition
    check_command_debian = """/bin/df -h /var/log/ | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /var/log/ | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38466(connection):
    stig_id = "V-38466"
    # The debian systems I tested did not have a /usr/lib64 directory, so I ignored it.
    check_command_debian = "/usr/bin/find -L /lib /lib64 /usr/lib \! -user root"
    check_command_redhat = "/bin/find -L /lib /lib64 /usr/lib /usr/lib64 \! -user root"
    fix_command_debian = "/usr/bin/find -L /lib /lib64 /usr/lib \! -user root -exec /bin/chown root {} \;"
    fix_command_redhat = "/bin/find -L /lib /lib64 /usr/lib /usr/lib64 \! -user root -exec /bin/chown root {} \;"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38467(connection):
    stig_id = "V-38467"
    # If anything is returned, this is a finding
    check_command_debian = """/bin/df -h /var/log/audit | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /var/log/audit | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38469(connection):
    stig_id = "V-38469"
    check_command_debian = "/usr/bin/find -L " \
                           "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                           "-perm /022 -type f"
    check_command_redhat = "/bin/find -L " \
                           "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                           "-perm /022 -type f"
    fix_command_debian = "/usr/bin/find -L " \
                         "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                         "-perm /022 -type f -exec /bin/chmod go-w {} \;"
    fix_command_redhat = "/bin/find -L " \
                         "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                         "-perm /022 -type f -exec /bin/chmod go-w {} \;"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38470(connection):
    stig_id = "V-38470"
    # NOTE: auditd may need to be installed on debian systems
    # This sed command returns the value of the space_left_action directive. A properly configured system
    # will display "email" according to the STIG requirements
    check_command_debian = "/bin/sed -n 's/^space_left_action\s=\s\(.*\)/\1/p' /etc/audit/auditd.conf"
    check_command_redhat = "/bin/sed -n 's/^space_left_action\s=\s\(.*\)/\1/p' /etc/audit/auditd.conf"
    fix_command_debian = """/usr/bin/dpkg -s auditd &&
                           /bin/sed -i 's/^\(space_left_action\s=\s\).*/\1email/' /etc/audit/audit.conf"""
    fix_command_redhat = "/bin/sed -i 's/^\(space_left_action\s=\s\).*/\1email/' /etc/audit/audit.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38472(connection):
    stig_id = "V-38472"
    check_command_debian = "/usr/bin/find -L" \
                           "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                           "\! -user root"
    check_command_redhat = "/bin/find -L " \
                           "/bin /usr/bin /usr/local/bin /sbin /usr/sbin /usr/local/sbin " \
                           "\! -user root"
    fix_command_debian = check_command_debian + " -exec {} \;"
    fix_command_redhat = check_command_redhat + "-exec {} \;"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38473(connection):
    stig_id = "V-38473"
    # if anything is returned, this is a finding
    check_command_debian = """/bin/df -h /home | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /home | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38475(connection):
    stig_id = "V-38475"
    # This is more of a script, but command with print text if the PASS_MIN_LEN directive is commented out, or the
    # directive is set to a value less than 14.
    check_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_LEN\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MIN_LEN.*\)/p' /etc/login.defs | /usr/bin/awk -F " " '{ \
        if (/#/) { print "Password length not set." } \
        else if ($2 < 14) {print "Password length too short."}}'; \
        fi
    """
    check_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_LEN\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MIN_LEN.*\)/p' /etc/login.defs | /bin/awk -F " " '{ \
        if (/#/) { print "Password length not set." } \
        else if ($2 < 14) {print "Password length too short."}}'; \
        fi
    """
    fix_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_LEN\>/p' /etc/login.defs) ]];then \
        echo "PASS_MIN_LEN    14" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_MIN_LEN\).*/\1    14/' /etc/login.defs;fi
    """
    fix_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_LEN\>/p' /etc/login.defs) ]];then \
        echo "PASS_MIN_LEN    14" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\(PASS_MIN_LEN\).*/\1    14/' /etc/login.defs;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38477(connection):
    stig_id = "V-38477"
    # Output of the following command will be null if PASS_MIN_DAYS is set to 1 or more.
    check_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_DAYS\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MIN_DAYS.*\)/p' /etc/login.defs | /usr/bin/awk -F " " '{ \
        if (/#/) { print "Min days not set." } \
        else if ($2 < 1) {print "One or more days must be set."}}'; \
        fi
        """
    check_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_DAYS\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MIN_DAYS.*\)/p' /etc/login.defs | /bin/awk -F " " '{ \
        if (/#/) { print "Min days not set." } \
        else if ($2 < 1) {print "One or more days must be set."}}'; \
        fi
        """
    fix_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_DAYS\>/p' /etc/login.defs) ]];then \
        echo "PASS_MIN_DAYS    1" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_MIN_DAYS\).*/\1    1/' /etc/login.defs;fi
    """
    fix_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MIN_DAYS\>/p' /etc/login.defs) ]];then \
        echo "PASS_MIN_DAYS    1" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_MIN_DAYS\).*/\1    1/' /etc/login.defs;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38478(connection):
    stig_id = "V-38478"
    # Not relevant on debian
    check_command_debian = "None"
    # Exit code will be zero if found, 1 if not
    check_command_redhat = "/sbin/chkconfig --list rhnsd | grep -o \"[2345]:on\""
    fix_command_debian = "None"
    fix_command_redhat = "/sbin/chkconfig rhnsd off && /sbin/service rhnsd stop"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38479(connection):
    stig_id = "V-38479"
    # Output of the following command will be null if PASS_MIN_DAYS is set to 60 or less.
    check_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MAX_DAYS\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MAX_DAYS.*\)/p' /etc/login.defs | /usr/bin/awk -F " " '{ \
        if (/#/) { print "Max days not set." } \
        else if ($2 > 60) {print "Password expiration should not exceed 60 days."}}'; \
        fi
    """
    check_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MAX_DAYS\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_MAX_DAYS.*\)/p' /etc/login.defs | /bin/awk -F " " '{ \
        if (/#/) { print "Max days not set." } \
        else if ($2 > 60) {print "Password expiration should not exceed 60 days."}}'; \
        fi
    """
    fix_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_MAX_DAYS\>/p' /etc/login.defs) ]];then \
        echo "PASS_MAX_DAYS    60" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_MAX_DAYS\).*/\1    60/' /etc/login.defs;fi
    """
    fix_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_MAX_DAYS\>/p' /etc/login.defs) ]];then \
        echo "PASS_MAX_DAYS    60" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_MAX_DAYS\).*/\1    60/' /etc/login.defs;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38480(connection):
    stig_id = "V-38480"
    # Output of the following command will be null if PASS_WARN_AGE is set to 7.
    check_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_WARN_AGE\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_WARN_AGE.*\)/p' /etc/login.defs | /usr/bin/awk -F " " '{ \
        if (/#/) { print "Pass warn days not set." } \
        else if ($2 != 7) {print "Password warn days should be 7."}}'; \
        fi
    """
    check_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_WARN_AGE\>/p' /etc/login.defs) ]]; \
        then echo "Directive not found."; \
        else /bin/sed -n '/\(^#\?PASS_WARN_AGE.*\)/p' /etc/login.defs | /bin/awk -F " " '{ \
        if (/#/) { print "Pass warn days not set." } \
        else if ($2 != 7) {print "Password warn days should be 7."}}'; \
        fi
    """
    fix_command_debian = """
        if [[ -z $(/bin/sed -n '/\<PASS_WARN_AGE\>/p' /etc/login.defs) ]];then \
        echo "PASS_MAX_DAYS    7" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_WARN_AGE\).*/\1    7/' /etc/login.defs;fi
    """
    fix_command_redhat = """
        if [[ -z $(/bin/sed -n '/\<PASS_WARN_AGE\>/p' /etc/login.defs) ]];then \
        echo "PASS_MAX_DAYS    7" >> /etc/login.defs;else \
        /bin/sed -i 's/^#\?\s\?\(PASS_WARN_AGE\).*/\1    7/' /etc/login.defs;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38482(connection):
    stig_id = "V-38482"
    check_command_debian = "None"
    # Returns a 0 if set properly
    check_command_redhat = "/bin/grep dcredit=-1 /etc/pam.d/system-auth"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/pam_cracklib.so/pam_cracklib.so dcredit=-1/' /etc/pam.d/system-auth"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38483(connection):
    stig_id = "V-38483"
    check_command_debian = "None"
    # Returns 0 if found
    check_command_redhat = "/bin/grep gpgcheck=1 /etc/yum.conf"
    fix_command_debian = "None"
    fix_command_redhat = """
        if [[ -z $(/bin/grep gpgcheck /etc/yum.conf) ]];then \
        /bin/echo "gpgcheck=1" >> /etc/yum.conf; \
        else /bin/sed -i 's/gpgcheck=./gpgcheck=1/' /etc/yum.conf;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38487(connection):
    stig_id = "V-38487"
    check_command_debian = "None"
    check_command_redhat = "/bin/grep \"gpgcheck=0\" /etc/yum.conf"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i '/gpgcheck=0/d' /etc/yum.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38489(connection):
    stig_id = "V-38489"
    check_command_debian = ""
    check_command_redhat = "/bin/rpm -qa | grep aide"
    fix_command_debian = ""
    fix_command_redhat = "/usr/bin/yum install aide"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38490(connection):
    stig_id = "V-38490"
    check_command_debian = ""
    check_command_redhat = "/bin/grep -ir \"install usb-storage /bin/true\" /etc/modprobe.d/"
    fix_command_debian = ""
    fix_command_redhat = "/bin/echo \"install usb-storage /bin/true\" > /etc/modprobe.d/usb-disable.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38491(connection):
    stig_id = "V-38491"
    check_command_debian = "/usr/bin/find /home /etc \( -name \".rhosts\" -o -name \"hosts.equiv\" \)"
    check_command_redhat = "/bin/find /home /etc \( -name \".rhosts\" -o -name \"hosts.equiv\" \)"
    fix_command_debian = "/usr/bin/find /home /etc \( -name \".rhosts\" -o -name \"hosts.equiv\" \) -exec rm {} \;"
    fix_command_redhat = "/bin/find /home /etc \( -name \".rhosts\" -o -name \"hosts.equiv\" \) -exec rm {} \;"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38492(connection):
    stig_id = "V-38492"
    check_command_debian = "/bin/grep \"^vc/*\" /etc/securetty"
    check_command_redhat = "/bin/grep \"^vc/*\" /etc/securetty"
    fix_command_debian = "/bin/sed -i '/^vc\/.*/d' /etc/securetty"
    fix_command_redhat = "/bin/sed -i '/^vc\/.*/d' /etc/securetty"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38494(connection):
    stig_id = "V-38494"
    check_command_debian = "/bin/grep \"ttyS.*\" /etc/securetty"
    check_command_redhat = "/bin/grep \"ttyS.*\" /etc/securetty"
    fix_command_debian = "/bin/sed -i '/^ttyS.*/d' /etc/securetty"
    fix_command_redhat = "/bin/sed -i '/^ttyS.*/d' /etc/securetty"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38495(connection):
    stig_id = "V-38495"
    check_command_debian = "/bin/grep \"^log_file\" /etc/audit/auditd.conf|/bin/sed s/^[^\/]*//|" \
                           "/usr/bin/xargs /usr/bin/stat -c %U:%n " \
                           "| /usr/bin/awk -F \":\" '{if ($1 != \"root\") {print $2}}'"
    check_command_redhat = "/bin/grep \"^log_file\" /etc/audit/auditd.conf|/bin/sed s/^[^\/]*//|" \
                           "/usr/bin/xargs /usr/bin/stat -c %U:%n " \
                           "| /bin/awk -F \":\" '{if ($1 != \"root\") {print $2}}'"
    fix_command_debian = "/bin/chown root $(/bin/grep \"^log_file\" /etc/audit/auditd.conf|/bin/sed s/^[^\/]*//" \
                         "|/usr/bin/xargs /usr/bin/stat -c %U:%n | /usr/bin/awk -F \":\" '{print $2}')"
    fix_command_redhat = "/bin/chown root $(/bin/grep \"^log_file\" /etc/audit/auditd.conf|/bin/sed s/^[^\/]*//" \
                         "|/usr/bin/xargs /usr/bin/stat -c %U:%n | /bin/awk -F \":\" '{print $2}')"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38497(connection):
    stig_id = "V-38497"
    check_command_debian = "None"
    check_command_redhat = "/bin/grep nullok /etc/pam.d/system-auth /etc/pam.d/system-auth-ac"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/\snullok//' /etc/pam.d/system-auth /etc/pam.d/system-auth-ac"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38498(connection):
    stig_id = "V-38498"
    check_command_debian = """
        /bin/grep "^log_file" /etc/audit/auditd.conf|/bin/sed s/^[^\/]*//|/usr/bin/xargs /usr/bin/stat -c %a|
        /usr/bin/awk '{if ($NF != 640) {print "Incorrect permissions " $NF}}'
    """
    check_command_redhat = """
        /bin/grep "^log_file" /etc/audit/auditd.conf|sed s/^[^\/]*//|/usr/bin/xargs /usr/bin/stat -c %a| \
        /bin/awk '{if ($NF != 640) {print "Incorrect permissions " $NF}}'
    """
    fix_command_debian = "/bin/chmod 0640 $(/bin/grep \"^log_file\" /etc/audit/auditd.conf" \
                         "|/bin/sed s/^[^\/]*//|/usr/bin/xargs /usr/bin/stat -c %n)"
    fix_command_redhat = "/bin/chmod 0640 $(/bin/grep \"^log_file\" /etc/audit/auditd.conf" \
                         "|/bin/sed s/^[^\/]*//|/usr/bin/xargs /usr/bin/stat -c %n)"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38499(connection):
    stig_id = "V-38499"
    # If anything other than x is stored in the second field, it is printed and assumed to be crypted passwd
    check_command_debian = "/usr/bin/awk -F \":\" '{if ($2 != \"x\") {print $2}}' /etc/passwd"
    check_command_redhat = "/bin/awk -F \":\" '{if ($2 != \"x\") {print $2}}' /etc/passwd"
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38500(connection):
    stig_id = "V-38500"
    check_command_debian = "/usr/bin/awk -F \":\" '{if ($3 == \"0\" && $1 != \"root\") {print $1}}' /etc/passwd"
    check_command_redhat = "/bin/awk -F \":\" '{if ($3 == \"0\" && $1 != \"root\") {print $1}}' /etc/passwd"
    fix_command_debian = "/usr/sbin/userdel $(/usr/bin/awk -F \":\" " \
                         "'{if ($3 == \"0\" && $1 != \"root\") {print $1}}' /etc/passwd)"
    fix_command_redhat = "/usr/sbin/userdel $(/bin/awk -F \":\" " \
                         "'{if ($3 == \"0\" && $1 != \"root\") {print $1}}' /etc/passwd)"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38501(connection):
    stig_id = "V-38501"
    check_command_debian = "None"
    check_command_redhat = "/bin/grep \"fail_interval\" /etc/pam.d/system-auth-ac"
    fix_command_debian = ""
    fix_command_redhat = """
        /bin/sed -i '/^auth.*pam_unix\.so/a \
        auth [default=die] pam_faillock.so authfail deny=3 unlock_time=604800 fail_interval=900\n \
        auth required pam_faillock.so authsucc deny=3 unlock_time=604800 fail_interval=900' \
        /etc/pam.d/system-auth-ac
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38502(connection):
    stig_id = "V-38502"
    check_command_debian = "/usr/bin/find /etc/shadow -user root"
    check_command_redhat = "/bin/find /etc/shadow -user root"
    fix_command_debian = "/bin/chown root /etc/shadow"
    fix_command_redhat = "/bin/chown root /etc/shadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38503(connection):
    stig_id = "V-38503"
    check_command_debian = "/usr/bin/find /etc/shadow -group root"
    check_command_redhat = "/bin/find /etc/shadow -group root"
    fix_command_debian = "/bin/chgrp root /etc/shadow"
    fix_command_redhat = "/bin/chgrp root /etc/shadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38504(connection):
    stig_id = "V-38504"
    # exit code should be 0, and contain the string /etc/shadow
    check_command_debian = "/usr/bin/find /etc/shadow -perm 0000"
    check_command_redhat = "/bin/find /etc/shadow -perm 0000"
    fix_command_debian = "/bin/chmod 0000 /etc/shadow"
    fix_command_redhat = "/bin/chmod 0000 /etc/shadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38511(connection):
    stig_id = "V-38511"
    check_command_debian = "/sbin/sysctl -a | grep \"net.ipv4.ip_forward\s\?=\s\?0\""
    check_command_redhat = "/sbin/sysctl -a | grep \"net.ipv4.ip_forward\s\?=\s\?0\""
    fix_command_debian = "/bin/echo \"net.ipv4.ip_forward = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.ip_forward = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38512(connection):
    stig_id = "V-38512"
    # TODO: in debian systems this isn't needed right?
    check_command_debian = "None"
    check_command_redhat = "/sbin/chkconfig --list iptables | /bin/grep \"[2-5]:on\""
    fix_command_debian = "None"
    fix_command_redhat = "/sbin/chkconfig iptables on && /sbin/service iptables start"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38513(connection):
    stig_id = "V-38513"
    check_command_debian = ""
    check_command_redhat = "/bin/grep \"^:INPUT DROP \[0:0\]\" /etc/sysconfig/iptables"
    fix_command_debian = ""
    fix_command_redhat = """
        if [[ -n $(/bin/grep "^:INPUT ACCEPT \[0:0\]" /etc/sysconfig/iptables) ]];then \
        /bin/sed -i 's/:INPUT ACCEPT \[0:0\]/:INPUT DROP \[0:0\]/' /etc/sysconfig/iptables; \
        elif [[ -z $(/bin/grep "^:INPUT DROP \[0:0\]" /etc/sysconfig/iptables)  ]];then \
        /bin/sed -i '/\*filter/a:INPUT DROP \[0:0\]' /etc/sysconfig/iptables;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38514(connection):
    stig_id = "V-38514"
    check_command_debian = "/bin/grep -ir \"install dccp /bin/true\" /etc/modprobe.d"
    check_command_redhat = "/bin/grep -ir \"install dccp /bin/true\" /etc/modprobe.d"
    fix_command_debian = "/bin/echo \"install dccp /bin/true\" > /etc/modprobe.d/dccp-load.conf"
    fix_command_redhat = "/bin/echo \"install dccp /bin/true\" > /etc/modprobe.d/dccp-load.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38515(connection):
    stig_id = "V-38515"
    check_command_debian = "/bin/grep -ir \"install sctp /bin/true\" /etc/modprobe.d"
    check_command_redhat = "/bin/grep -ir \"install sctp /bin/true\" /etc/modprobe.d"
    fix_command_debian = "/bin/echo \"install sctp /bin/true\" > /etc/modprobe.d/sctp-load.conf"
    fix_command_redhat = "/bin/echo \"install sctp /bin/true\" > /etc/modprobe.d/sctp-load.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38516(connection):
    stig_id = "V-38516"
    check_command_debian = "/bin/grep -ir \"install rds /bin/true\" /etc/modprobe.d"
    check_command_redhat = "/bin/grep -ir \"install rds /bin/true\" /etc/modprobe.d"
    fix_command_debian = "/bin/echo \"install rds /bin/true\" > /etc/modprobe.d/rds-load.conf"
    fix_command_redhat = "/bin/echo \"install rds /bin/true\" > /etc/modprobe.d/rds-load.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38517(connection):
    stig_id = "V-38517"
    check_command_debian = "/bin/grep -ir \"install tipc /bin/true\" /etc/modprobe.d"
    check_command_redhat = "/bin/grep -ir \"install tipc /bin/true\" /etc/modprobe.d"
    fix_command_debian = "/bin/echo \"install tipc /bin/true\" > /etc/modprobe.d/tipc-load.conf"
    fix_command_redhat = "/bin/echo \"install tipc /bin/true\" > /etc/modprobe.d/tipc-load.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38518(connection):
    stig_id = "V-38518"
    check_command_debian = """
        /bin/grep -o '\/\(dev\|var\)\/[a-zA-Z\/0-9\.]*' /etc/rsyslog.conf | /usr/bin/xargs /usr/bin/stat -c %n:%U
    """
    check_command_redhat = """
        /bin/grep -o '\/\(dev\|var\)\/[a-zA-Z\/0-9\.]*' /etc/rsyslog.conf | /usr/bin/xargs /usr/bin/stat -c %n:%U
    """
    fix_command_debian = """
        /bin/chown -R root $(/bin/grep -o '\/\(dev\|var\)\/[a-zA-Z\/0-9\.]*' /etc/rsyslog.conf) && \
        /bin/sed -i 's/^\(\$\(File\|PrivDropTo\)\(Owner\|Group\|User\)\s\+\).*/\1root/' /etc/rsyslog.conf
    """
    fix_command_redhat = """
        /bin/chown -R root $(/bin/grep -o '\/\(dev\|var\)\/[a-zA-Z\/0-9\.]*' /etc/rsyslog.conf)
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38520(connection):
    stig_id = "V-38520"
    # The user will manually have to configure a remote syslog server.
    check_command_debian = "/bin/grep -o '^\*\.\*\s\(:omrelp\|@\|@@\).*' /etc/rsyslog.conf"
    check_command_redhat = "/bin/grep -o '^\*\.\*\s\(:omrelp\|@\|@@\).*' /etc/rsyslog.conf"
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38521(connection):
    stig_id = "V-38521"
    # The user will manually have to configure a remote syslog server.
    check_command_debian = "/bin/grep -o '^\*\.\*\s\(:omrelp\|@\|@@\).*' /etc/rsyslog.conf"
    check_command_redhat = "/bin/grep -o '^\*\.\*\s\(:omrelp\|@\|@@\).*' /etc/rsyslog.conf"
    fix_command_debian = "None"
    fix_command_redhat = "None"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38522(connection):
    stig_id = "V-38522"
    # Auditd is probally not installed on debian systems by default
    check_command_debian = "/sbin/auditctl -l | /bin/grep settimeofday"
    check_command_redhat = "/sbin/auditctl -l | /bin/grep settimeofday"
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then \
        /bin/echo "-a always,exit -F arch=b64 -S settimeofday -k audit_time_rules" >> \
        /etc/audit/audit.rules;else \
        /bin/echo "-a always,exit -F arch=b32 -S settimeofday -k audit_time_rules" >> /etc/audit/audit.rules;fi
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then \
        /bin/echo "-a always,exit -F arch=b64 -S settimeofday -k audit_time_rules" >> \
        /etc/audit/audit.rules;else \
        /bin/echo "-a always,exit -F arch=b32 -S settimeofday -k audit_time_rules" >> /etc/audit/audit.rules;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38523(connection):
    stig_id = "V-38523"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.all.accept_source_route\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.all.accept_source_route\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.all.accept_source_route = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.all.accept_source_route = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38524(connection):
    stig_id = "V-38524"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.all.accept_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.all.accept_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.all.accept_redirects = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.all.accept_redirects = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38525(connection):
    stig_id = "V-38525"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86" ]];then \
        /sbin/auditctl -l | grep stime;fi
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86" ]];then \
        /sbin/auditctl -l | grep stime;fi
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86" ]];then \
        /bin/echo "-a always,exit -F arch=b32 -S stime -k audit_time_rules" >> \
        /etc/audit/audit.rules;fi
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86" ]];then \
        /bin/echo "-a always,exit -F arch=b32 -S stime -k audit_time_rules" >> \
        /etc/audit/audit.rules;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38526(connection):
    stig_id = "V-38526"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.all.secure_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.all.secure_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.all.secure_redirects = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.all.secure_redirects = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38527(connection):
    stig_id = "V-38527"
    check_command_debian = "/sbin/auditctl -l | /bin/grep clock_settime"
    check_command_redhat = "/sbin/auditctl -l | /bin/grep clock_settime"
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then \
        /bin/echo "-a always,exit -F arch=b64 -S clock_settime -k audit_time_rules" >> \
        /etc/audit/audit.rules;else \
        /bin/echo "-a always,exit -F arch=b32 -S clock_settime -k audit_time_rules" >> /etc/audit/audit.rules;fi
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then \
        /bin/echo "-a always,exit -F arch=b64 -S clock_settime -k audit_time_rules" >> \
        /etc/audit/audit.rules;else \
        /bin/echo "-a always,exit -F arch=b32 -S clock_settime -k audit_time_rules" >> /etc/audit/audit.rules;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38528(connection):
    stig_id = "V-38528"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.all.log_martians\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.all.log_martians\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.all.log_martians = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.all.log_martians = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38529(connection):
    stig_id = "V-38529"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.default.accept_source_route\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.default.accept_source_route\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.default.accept_source_route = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.default.accept_source_route = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38530(connection):
    stig_id = "V-38530"
    check_command_debian = "/bin/grep \"audit_time_rules\" /etc/audit/audit.rules"
    check_command_redhat = "/bin/grep \"audit_time_rules\" /etc/audit/audit.rules"
    fix_command_debian = "/bin/echo \"-w /etc/localtime -p wa -k audit_time_rules\" >> /etc/audit/audit.rules"
    fix_command_redhat = "/bin/echo \"-w /etc/localtime -p wa -k audit_time_rules\" >> /etc/audit/audit.rules"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38531(connection):
    stig_id = "V-38531"
    check_command_debian = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    check_command_redhat = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    fix_command_debian = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38532(connection):
    stig_id = "V-38532"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.default.secure_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.default.secure_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.default.secure_redirects = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.default.secure_redirects = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38533(connection):
    stig_id = "V-38533"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.default.accept_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.default.accept_redirects\s\+\?=\s\+\?0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.default.accept_redirects = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.default.accept_redirects = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38534(connection):
    stig_id = "V-38534"
    check_command_debian = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    check_command_redhat = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    fix_command_debian = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38535(connection):
    stig_id = "V-38535"
    check_command_debian = "/bin/grep \"^net.ipv4.icmp_echo_ignore_broadcasts\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.icmp_echo_ignore_broadcasts\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.icmp_echo_ignore_broadcasts = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.icmp_echo_ignore_broadcasts = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38536(connection):
    stig_id = "V-38536"
    check_command_debian = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    check_command_redhat = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    fix_command_debian = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38537(connection):
    stig_id = "V-38537"
    check_command_debian = "/bin/grep \"^net.ipv4.icmp_ignore_bogus_error_responses\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.icmp_ignore_bogus_error_responses\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.icmp_ignore_bogus_error_responses = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.icmp_ignore_bogus_error_responses = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38538(connection):
    stig_id = "V-38538"
    check_command_debian = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    check_command_redhat = """
        /bin/grep -e "-w /etc/group -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/passwd -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/gshadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/shadow -p wa -k audit_account_changes" /etc/audit/audit.rules && \
        /bin/grep -e "-w /etc/security/opasswd -p wa -k audit_account_changes" /etc/audit/audit.rules
    """
    fix_command_debian = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        /bin/echo -e "-w /etc/group -p wa -k audit_account_changes\n-w /etc/passwd -p wa -k audit_account_changes\n-w /etc/gshadow -p wa -k audit_account_changes\n-w /etc/shadow -p wa -k audit_account_changes\n-w /etc/security/opasswd -p wa -k audit_account_changes" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38539(connection):
    stig_id = "V-38539"
    check_command_debian = "/bin/grep \"^net.ipv4.tcp_syncookies\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.tcp_syncookies\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.tcp_syncookies = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.tcp_syncookies = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38541(connection):
    stig_id = "V-38541"
    check_command_debian = "/bin/grep -e \"-w /etc/selinux/ -p wa -k MAC-policy\" /etc/audit/audit.rules"
    check_command_redhat = "/bin/grep -e \"-w /etc/selinux/ -p wa -k MAC-policy\" /etc/audit/audit.rules"
    fix_command_debian = "/bin/echo \"-w /etc/selinux/ -p wa -k MAC-policy\" >> /etc/audit/audit.rules"
    fix_command_redhat = "/bin/echo \"-w /etc/selinux/ -p wa -k MAC-policy\" >> /etc/audit/audit.rules"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38542(connection):
    stig_id = "V-38542"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.all.rp_filter\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.all.rp_filter\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"^net.ipv4.conf.all.rp_filter = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"^net.ipv4.conf.all.rp_filter = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38543(connection):
    stig_id = "V-38543"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chmod -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chmod -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chmod -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chmod -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chmod -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chmod -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chmod -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chmod -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38544(connection):
    stig_id = "V-38544"
    check_command_debian = "/bin/grep \"^net.ipv4.conf.default.rp_filter\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep \"^net.ipv4.conf.default.rp_filter\s\+\?=\s\+\?1\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo \"net.ipv4.conf.default.rp_filter = 1\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo \"net.ipv4.conf.default.rp_filter = 1\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38545(connection):
    stig_id = "38545"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S chown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S chown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38546(connection):
    stig_id = "V-38546"
    check_command_debian = "/bin/grep -re \"options ipv6 disable\s*=\s*1\" /etc/modprobe.d/"
    check_command_redhat = "/bin/grep -re \"options ipv6 disable\s*=\s*1\" /etc/modprobe.d/"
    fix_command_debian = "/bin/echo \"options ipv6 disable=1\" > /etc/modprobe.d/ipv6-disable.conf"
    fix_command_redhat = "/bin/echo \"options ipv6 disable=1\" > /etc/modprobe.d/ipv6-disable.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38547(connection):
    stig_id = "V-38547"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmod -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38548(connection):
    stig_id = "38548"
    check_command_debian = "/bin/grep -e \"net\.ipv6\.conf\.default\.accept_redirects\s*=\s*0\" /etc/sysctl.conf"
    check_command_redhat = "/bin/grep -e \"net\.ipv6\.conf\.default\.accept_redirects\s*=\s*0\" /etc/sysctl.conf"
    fix_command_debian = "/bin/echo -e \"net.ipv6.conf.default.accept_redirects = 0\" >> /etc/sysctl.conf"
    fix_command_redhat = "/bin/echo -e \"net.ipv6.conf.default.accept_redirects = 0\" >> /etc/sysctl.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38550(connection):
    stig_id = "V-38550"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchmodat -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38552(connection):
    stig_id = "V-38552"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38554(connection):
    stig_id = "V-38554"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fchownat -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38555(connection):
    stig_id = "V-38555"
    check_command_debian = "None"
    check_command_redhat = "/sbin/chkconfig --list iptables | /bin/grep -o \"[2345]:on\""
    fix_command_debian = "None"
    fix_command_redhat = "/sbin/chkconfig iptables on && /sbin/service iptables start"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38556(connection):
    stig_id = "V-38556"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fremovexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38557(connection):
    stig_id = "V-38557"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S fsetxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38558(connection):
    stig_id = "V-38558"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lchown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lchown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lchown -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lchown -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lchown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lchown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lchown -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lchown -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38559(connection):
    stig_id = "V-38559"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lremovexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38561(connection):
    stig_id = "V-38561"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S lsetxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38563(connection):
    stig_id = "V-38563"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S removexattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38565(connection):
    stig_id = "V-38565"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S setxattr -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38568(connection):
    stig_id = "V-38568"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S mount -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S mount -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S mount -F auid>=500 -F auid!=4294967295 -k perm_mod" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S mount -F auid=0 -k perm_mod" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S mount -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S mount -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S mount -F auid>=500 -F auid!=4294967295 -k perm_mod" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S mount -F auid=0 -k perm_mod" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38569(connection):
    stig_id = "V-38569"
    check_command_debian = "None"
    # Returns a 0 if set properly
    check_command_redhat = "/bin/grep ucredit=-1 /etc/pam.d/system-auth"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/pam_cracklib.so/pam_cracklib.so ucredit=-1/' /etc/pam.d/system-auth"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38570(connection):
    stig_id = "V-38570"
    check_command_debian = "None"
    # Returns a 0 if set properly
    check_command_redhat = "/bin/grep ocredit=-1 /etc/pam.d/system-auth"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/pam_cracklib.so/pam_cracklib.so ocredit=-1/' /etc/pam.d/system-auth"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38571(connection):
    stig_id = "V-38571"
    check_command_debian = "None"
    # Returns a 0 if set properly
    check_command_redhat = "/bin/grep lcredit=-1 /etc/pam.d/system-auth"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/pam_cracklib.so/pam_cracklib.so lcredit=-1/' /etc/pam.d/system-auth"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38572(connection):
    stig_id = "V-38572"
    check_command_debian = "None"
    # Returns a 0 if set properly
    check_command_redhat = "/bin/grep difok=4 /etc/pam.d/system-auth"
    fix_command_debian = "None"
    fix_command_redhat = "/bin/sed -i 's/pam_cracklib.so/pam_cracklib.so difok=4/' /etc/pam.d/system-auth"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38573(connection):
    stig_id = "V-38573"
    check_command_debian = "None"
    check_command_redhat = """/bin/grep \"fail_interval\" /etc/pam.d/system-auth-ac && \
        /bin/grep \"fail_interval\" /etc/pam.d/password-auth-ac
    """
    fix_command_debian = "None"
    fix_command_redhat = """
        /bin/sed -i '/^auth.*pam_unix\.so/a \
        auth [default=die] pam_faillock.so authfail deny=3 unlock_time=604800 fail_interval=900\n \
        auth required pam_faillock.so authsucc deny=3 unlock_time=604800 fail_interval=900' \
        /etc/pam.d/system-auth-ac /etc/pam.d/password-auth-ac
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38574(connection):
    stig_id = "V-38574"
    check_command_debian = "None"
    check_command_redhat = """
        /bin/grep sha512 /etc/pam.d/system-auth
    """
    fix_command_debian = "None"
    fix_command_redhat = """
        /bin/sed -i 's/^\(password\s*sufficient\s*pam_unix.so\)/\1 sha512/' /etc/pam.d/system-auth
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38575(connection):
    stig_id = "V-38575"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=ARCH -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid>=500 -F auid!=4294967295 -k delete" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=ARCH -S rmdir -S unlink -S unlinkat -S rename -S renameat -F auid=0 -k delete" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38576(connection):
    stig_id = "V-38576"
    check_command_debian = "/bin/grep \"ENCRYPT_METHOD SHA512\" /etc/login.defs"
    check_command_redhat = "/bin/grep \"ENCRYPT_METHOD SHA512\" /etc/login.defs"
    fix_command_debian = """
        if [[ -z $(/bin/grep "ENCRYPT_METHOD" /etc/login.defs) ]];then \
        /bin/echo "ENCRYPT_METHOD SHA512" >> /etc/login.defs;else \
        /bin/sed -i 's/\(ENCRYPT_METHOD\s*\)\(.*\)/\1SHA512/' /etc/login.defs;fi
    """
    fix_command_redhat = """
        if [[ -z $(/bin/grep "ENCRYPT_METHOD" /etc/login.defs) ]];then \
        /bin/echo "ENCRYPT_METHOD SHA512" >> /etc/login.defs;else \
        /bin/sed -i 's/\(ENCRYPT_METHOD\s*\)\(.*\)/\1SHA512/' /etc/login.defs;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38577(connection):
    stig_id = "V-38577"
    check_command_debian = "None"
    check_command_redhat = "/bin/grep \"crypt_style = sha512\" /etc/libuser.conf"
    fix_command_debian = "None"
    fix_command_redhat = """
        if [[ -z $(/bin/grep "ENCRYPT_METHOD" /etc/login.defs) ]];then \
        /bin/echo "crypt_style = sha512" >> /etc/libuser.conf;else \
        /bin/sed -i 's/^\(crypt_style\s*=\s*\)\(.*\)/\1sha512/' /etc/libuser.conf;fi
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38578(connection):
    stig_id = "V-38578"
    check_command_debian = "/bin/grep \"-w /etc/sudoers -p wa -k actions\" /etc/audit/audit.rules"
    check_command_redhat = "/bin/grep \"-w /etc/sudoers -p wa -k actions\" /etc/audit/audit.rules"
    fix_command_debian = "/bin/echo -e \"-w /etc/sudoers -p wa -k actions\" >> /etc/audit/audit.rules"
    fix_command_redhat = "/bin/echo -e \"-w /etc/sudoers -p wa -k actions\" >> /etc/audit/audit.rules"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38579(connection):
    stig_id = "V-38579"
    check_command_debian = "/usr/bin/stat /etc/default/grub -c %U | /bin/grep root"
    check_command_redhat = "/usr/bin/stat /etc/grub.conf -c %U | /bin/grep root"
    fix_command_debian = "/bin/chown root /etc/default/grub"
    fix_command_redhat = "/bin/chown root /etc/grub.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38580(connection):
    stig_id = "V-38580"
    check_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-w /sbin/insmod -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-w /sbin/rmmod -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-w /sbin/modprobe -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S init_module -S delete_module -k modules" /etc/audit/audit.rules
    """
    check_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/grep -e "-w /sbin/insmod -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-w /sbin/rmmod -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-w /sbin/modprobe -p x -k modules" /etc/audit/audit.rules && \
        /bin/grep -e "-a always,exit -F arch=${ARCH} -S init_module -S delete_module -k modules" /etc/audit/audit.rules
    """
    fix_command_debian = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-w /sbin/insmod -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-w /sbin/rmmod -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-w /sbin/modprobe -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules
    """
    fix_command_redhat = """
        if [[ $(/bin/uname -i) == "x86_64" ]];then ARCH=b64;else ARCH=b32;fi && \
        /bin/echo -e "-w /sbin/insmod -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-w /sbin/rmmod -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-w /sbin/modprobe -p x -k modules" >> /etc/audit/audit.rules && \
        /bin/echo -e "-a always,exit -F arch=${ARCH} -S init_module -S delete_module -k modules" >> /etc/audit/audit.rules
    """
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38581(connection):
    stig_id = ""
    check_command_debian = "/usr/bin/stat /etc/default/grub -c %G | /bin/grep root"
    check_command_redhat = "/usr/bin/stat /etc/grub.conf -c %G | /bin/grep root"
    fix_command_debian = "/bin/chgrp root /etc/default/grub"
    fix_command_redhat = "/bin/chgrp root /etc/grub.conf"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38582(connection):
    stig_id = ""
    check_command_debian = ""
    check_command_redhat = ""
    fix_command_debian = ""
    fix_command_redhat = ""
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_(connection):
    stig_id = ""
    check_command_debian = ""
    check_command_redhat = ""
    fix_command_debian = ""
    fix_command_redhat = ""
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def main():
    conn = sqlite3.connect("linux_stig.db")

    # Insertion of stig data into database
    stig_v_38437(conn)
    stig_v_38438(conn)
    stig_v_38448(conn)
    stig_v_38449(conn)
    stig_v_38450(conn)
    stig_v_38451(conn)
    stig_v_38455(conn)
    stig_v_38456(conn)
    stig_v_38457(conn)
    stig_v_38458(conn)
    stig_v_38459(conn)
    stig_v_38461(conn)
    stig_v_38463(conn)
    stig_v_38466(conn)
    stig_v_38467(conn)
    stig_v_38469(conn)
    stig_v_38470(conn)
    stig_v_38472(conn)
    stig_v_38473(conn)
    stig_v_38475(conn)
    stig_v_38477(conn)
    stig_v_38478(conn)
    stig_v_38479(conn)
    stig_v_38480(conn)
    stig_v_38482(conn)
    stig_v_38483(conn)
    stig_v_38487(conn)
    stig_v_38489(conn)
    stig_v_38490(conn)
    stig_v_38491(conn)
    stig_v_38492(conn)
    stig_v_38494(conn)
    stig_v_38495(conn)
    stig_v_38497(conn)
    stig_v_38498(conn)
    stig_v_38499(conn)
    stig_v_38500(conn)
    stig_v_38501(conn)
    stig_v_38502(conn)
    stig_v_38503(conn)
    stig_v_38504(conn)
    stig_v_38511(conn)
    stig_v_38512(conn)
    stig_v_38513(conn)
    stig_v_38514(conn)
    stig_v_38515(conn)
    stig_v_38516(conn)
    stig_v_38517(conn)
    stig_v_38518(conn)
    stig_v_38520(conn)
    stig_v_38521(conn)
    stig_v_38522(conn)
    stig_v_38523(conn)
    stig_v_38524(conn)
    stig_v_38525(conn)
    stig_v_38526(conn)
    stig_v_38527(conn)
    stig_v_38528(conn)
    stig_v_38529(conn)
    stig_v_38530(conn)
    stig_v_38531(conn)
    stig_v_38532(conn)
    stig_v_38533(conn)
    stig_v_38534(conn)
    stig_v_38535(conn)
    stig_v_38536(conn)
    stig_v_38537(conn)
    stig_v_38538(conn)
    stig_v_38539(conn)
    stig_v_38541(conn)
    stig_v_38542(conn)
    stig_v_38543(conn)
    stig_v_38544(conn)
    stig_v_38545(conn)
    stig_v_38546(conn)
    stig_v_38547(conn)
    stig_v_38548(conn)
    stig_v_38550(conn)
    stig_v_38552(conn)
    stig_v_38554(conn)
    stig_v_38555(conn)
    stig_v_38556(conn)
    stig_v_38557(conn)
    stig_v_38558(conn)
    stig_v_38559(conn)
    stig_v_38561(conn)
    stig_v_38563(conn)
    stig_v_38565(conn)
    stig_v_38568(conn)
    stig_v_38569(conn)
    stig_v_38570(conn)
    stig_v_38571(conn)
    stig_v_38572(conn)
    stig_v_38573(conn)
    stig_v_38574(conn)
    stig_v_38575(conn)
    stig_v_38576(conn)
    stig_v_38577(conn)
    stig_v_38578(conn)
    stig_v_38579(conn)
    stig_v_38580(conn)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
