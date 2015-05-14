#!/usr/bin/expect -f
                               
set user [lindex $argv 0];
set hostname [lindex $argv 1];
set password [lindex $argv 2];
set prompt "devel@my ~ $ "
set rails_webapp "Alias /rails /var/lib/rails-app/public\n<Directory /var/lib/rails-app/public>\nAllow from all\nPassengerAppRoot \"/var/lib/rails-app/public\"\n</Directory>"
 
spawn ssh "${user}@${hostname}"
set timeout 3
expect "assword:"
send "$password\r"
expect "$"
send "sudo su -\r"
expect "assword:"
send "$password\r"
expect "#"
send "whoami\r"
send "rails new /var/lib/rails-app\r"
send "chown -R apache:apache /var/lib/rails-app\r"
send "echo -e '$rails_webapp' > /etc/httpd/conf.d/rails.webapp\r"
send "/etc/init.d/httpd restart\r"
exit
