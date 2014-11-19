__author__ = 'sdouglas'


import pxssh


rails_webapp = "Alias /rails /var/lib/rails-app/public\n" \
               "<Directory /var/lib/rails-app/public>\n" \
               "Allow from all\n" \
               "PassengerAppRoot \"/var/lib/rails-app/public\"\n" \
               "</Directory>"


def connect(host, username, password):
    try:
        c = pxssh.pxssh()
        c.login(host, username, password)
        return c
    except Exception, e:
        print "Error Connecting: \n" + str(e)


def main():
    ip = "10.1.252.86"
    user = "devel"
    user_password = "pass"
    c = connect(ip, user, user_password)
    command = "echo -e '%s' > /tmp/rails.webapp" % rails_webapp
    c.sendline(command)
    c.prompt()
    c.sendline("sudo su")
    c.expect('assword')
    c.prompt()
    c.sendline("pass")
    c.prompt()
    c.sendline("chmod 777 /tmp/rails.webapp")
    c.prompt()

if __name__ == '__main__':
    main()
