__author__ = 'sdouglas'


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
    fix_command_redhat = """/bin/sed -e 's/.*\(kernel\s.*\)/\1 audit=1/' /etc/grub.conf"""
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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
