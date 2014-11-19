#!/usr/bin/python
__author__ = 'sdouglas'
import os
import sys
import getopt
import re
from subprocess import *


USAGE = "Usage: rhel-local-repo.py -a\n" \
        "Tool for creating/removing a local rhel repo.\n" \
        "Run this script after attaching your iso.\n\n" \
        "   -a, --add           add local repo\n" \
        "   -c, --clean         remove files created\n" \
        "   -h, --help          display this message\n\n" \
        "Example:\n   rhel-local-repo -c"


def check_if_root():
    user_id = os.getuid()
    if user_id != 0:
        print "This script must be run as root!"
        sys.exit(1)


def check_for_createrepo():
    command = "/bin/rpm -q createrepo"
    output = Popen(command.split(), shell=False, stdout=PIPE).stdout.read().rstrip("\n")
    if output == "package createrepo is not installed":
        print "Please install createrepo and its dependencies (deltarpm & python-deltarpm)."
        exit()


def find_redhat_type():
    with open("/etc/redhat-release", "r") as release:
        redhat_release = release.read().rstrip("\n\r")
        capture = re.findall('(.*)\s.*\s([0-9]\.[0-9])\s', redhat_release)
        return capture


def gpg_key_type():
    release = find_redhat_type()
    if release[0][0] == "CentOS":
        return "RPM-GPG-KEY-CentOS-" + str(release[0][1])[0]
    else:
        return "RPM-GPG-KEY-redhat-release"


def create_repo():
    check_for_createrepo()
    gpg_key = gpg_key_type()

    repo_file = "[rhel-local]\n" \
      "name=RHEL local repository\n" \
      "baseurl=file:///opt/yum/rhel-local\n" \
      "gpgcheck=1\n" \
      "gpgkey=file:///etc/pki/rpm-gpg/%s\n" % gpg_key + \
      "enabled=1"

    copy_contents_to_local_path = [
        "mkdir -p /mnt/rhel-cd /opt/yum/rhel-local/repodata",
        "mount -o loop /dev/sr0 /mnt/rhel-cd",
        "cp -a /mnt/rhel-cd/Packages/*.rpm /opt/yum/rhel-local",
        "cp /mnt/rhel-cd/repodata/*comps*.xml /opt/yum/rhel-local/repodata/comps.xml",
        "createrepo -g /opt/yum/rhel-local/repodata/comps.xml /opt/yum/rhel-local/",
        "cp -r /etc/yum.repos.d/ /etc/yum.repos.d.old/",
        "rm -rf /etc/yum.repos.d/*",
        "echo '%s' > /etc/yum.repos.d/rhel-local.repo" % repo_file
    ]

    for command in copy_contents_to_local_path:
        try:
            Popen(command, shell=True, stdout=PIPE).stdout.read()
        except Exception as e:
            print e

    print "Your local repository has been established.\nPlease run:\n  yum clean all\nTo clear cached repository files."


def clean_up():
    clean_up_list = [
        "umount /mnt/rhel-cd",
        "rm -rf /mnt/rhel-cd /opt/yum /etc/yum.repos.d/",
        "mv /etc/yum.repos.d.old/ /etc/yum.repos.d/"
    ]

    for command in clean_up_list:
        try:
            Popen(command, shell=True, stdout=PIPE).stdout.read()
        except Exception as e:
            print e


def get_opts(argv):
    task = ''
    try:
        # Formatting used by getopt, it's slightly confusing. argv is the commandline args the user provides.
        # The second value defines which letter opts take arguments (e.g. -g), designated with a ':' after the char.
        # The third value defines which long form opts take arguments, designated with a '='.
        opts, args = getopt.getopt(argv, "hca", ["help", "clean", "add"])
    except getopt.GetoptError:
        # Print our usage constant if we find a problem.
        print USAGE
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print USAGE
            sys.exit()
        elif opt in ("-c", "--clean"):
            task = "clean"
        elif opt in ("-a", "--add"):
            task = "create"
    return {"Task": task}


def execute_tasks(options):
    if options['Task'] == 'clean':
        clean_up()
    elif options['Task'] == 'create':
        create_repo()
    else:
        print USAGE
        sys.exit()


def main():
    check_if_root()
    options = get_opts(sys.argv[1:])
    execute_tasks(options)


if __name__ == "__main__":
    main()