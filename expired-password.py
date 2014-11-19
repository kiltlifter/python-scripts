__author__ = 'sdouglas'


import pexpect
import optparse


PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_command(session, command):
    session.sendline(command)
    session.expect(PROMPT)
    print session.before


def connection(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    conection_string = "ssh %s@%s" % (user, host)
    session = pexpect.spawn(conection_string)
    ret_val = session.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret_val == 0:
        print "[-] Error connecting."
        return
    if ret_val == 1:
        session.sendline('yes')
        ret_val = session.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret_val == 0:
            print "[-] Error Connecting."
            return
    session.sendline(password)
    session.expect(PROMPT)
    return session


def main():
    parser = optparse.OptionParser("expired-password.py -h <host> -u <user>")
    parser.add_option('-h', dest='host', type='string', help='enter a host')
    parser.add_option('-u', dest='user', type='string', help='enter a user')
    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    old_pass = raw_input("Current password: ")
    new_pass = raw_input("New password: ")



if __name__ == '__main__':
    main()
