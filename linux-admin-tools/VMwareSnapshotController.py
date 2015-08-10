#!/usr/bin/python

import VMwareAssist as vmware_cli
import re
import sys


def read_builtins(file_name, vmware_obj):
    vmware = vmware_obj
    with open(file_name, "r") as f:
        for line in f:
            if re.search("^VM='.*'", line):
                vmware.target_machine = "".join(re.findall("^VM='(.*)'", line))
            elif re.search("^VM_IP='.*'", line):
                vm_ip_addr = "".join(re.findall("^VM_IP='(.*)'", line))
            elif re.search("^HOST_LIST=\(.*\)", line):
                vmware.esxi_host_list = re.findall("(\d+\.\d+\.\d+\.\d+)", line)
            elif re.search("^USER='.*'", line):
                vmware.esxi_user = "".join(re.findall("^USER='(.*)'", line))
                vmware.vcenter_user = vmware.esxi_user
            elif re.search("^HOST_PASSWORD='.*'", line):
                vmware.esxi_pass = "".join(re.findall("^HOST_PASSWORD='(.*)'", line))
            elif re.search("^VCENTER='.*'", line):
                vmware.vcenter_host = "".join(re.findall("^VCENTER='(.*)'", line))
            elif re.search("^VC_PASSWORD='.*'", line):
                vmware.vcenter_pass = "".join(re.findall("^VC_PASSWORD='(.*)'", line))
            else:
                continue
    return vmware


def main():
    try:
        builtins_path = sys.argv[1]
    except:
        print "Please specify the full path to the builtins.sh file"
        exit()

    vmware = read_builtins(builtins_path, vmware_cli.VMwareAssist())

    vm_host, vm_config = vmware.find_machine()

    print vm_host
    print vm_config
    #vmware.revert_snapshot(vm_host, vm_config)
    #vmware.take_snapshot(vm_host, vm_config, "python snap", "Test snapshot using python tool", "0", "0")
    print "done."


if __name__ == "__main__":
    main()
