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
                           "/usr/bin/find -L /etc/rc2.d /etc/rc3.d /etc/rc4.d /etc/rc5.d -name S*autofs*"
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
    check_command_debian = "/bin/find /etc/ -group root -name gshadow"
    check_command_redhat = "/bin/find /etc/ -group root -name gshadow"
    fix_command_debian = "/bin/chgrp root /etc/gshadow"
    fix_command_redhat = "/bin/chgrp root /etc/gshadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38449(connection):
    stig_id = "V-38449"
    check_command_debian = "/bin/find /etc/ -perm 0000 -name gshadow"
    check_command_redhat = "/bin/find /etc/ -perm 0000 -name gshadow"
    fix_command_debian = "/bin/chmod 0000 /etc/gshadow"
    fix_command_redhat = "/bin/chmod 0000 /etc/gshadow"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38450(connection):
    stig_id = "V-38450"
    check_command_debian = "/bin/find /etc/passwd -user root"
    check_command_redhat = "/bin/find /etc/passwd -user root"
    fix_command_debian = "/bin/chown root /etc/passwd"
    fix_command_redhat = "/bin/chown root /etc/passwd"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38451(connection):
    stig_id = "V-38451"
    check_command_debian = "/bin/find /etc/passwd -group root"
    check_command_redhat = "/bin/find /etc/passwd -group root"
    fix_command_debian = "/bin/chgrp root /etc/passwd"
    fix_command_redhat = "/bin/chgrp root /etc/passwd"
    values = [check_command_debian, check_command_redhat, fix_command_debian, fix_command_redhat, stig_id]
    update_row(connection, values)


def stig_v_38455(connection):
    stig_id = "V-38455"
    check_command_debian = """/bin/df -h /tmp | grep -i "mounted on"""
    check_command_redhat = """/bin/df -h /tmp | grep -i "mounted on"""
    fix_command_debian = "None"
    fix_command_redhat = "None"
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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
