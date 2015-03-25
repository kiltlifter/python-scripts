__author__ = 'sdouglas'


import re
from subprocess import *


class VMwareAssist():
    def __init__(self):
        self.esxi_host_list = []   # Hosts within you vSphere environement
        self.esxi_user = ""        # esxi username
        self.esxi_pass = ""        # esxi password
        self.vcenter_host = ""     # Machine used to access vSphere client
        self.vcenter_user = ""     # vSphere username
        self.vcenter_pass = ""     # vSphere password
        self.vmware_cmd = "/opt/vmware/bin/vmware-cmd"
        self.esxcli_tool = "/usr/bin/esxcli"
        self.target_machine = ""

    def find_machine(self):
        display_name_regex = re.compile('Display Name:\s(.*)\n')
        config_file_regex = re.compile(self.target_machine + '\n\s+Config File:\s(.*.vmx)')
        target_info = []
        for host in self.esxi_host_list:
            find_host_cmd = "%s --server %s --username %s --password %s vms vm list" % (self.esxcli_tool, host, self.esxi_user, self.esxi_pass)
            vm_listing_raw = Popen(find_host_cmd.split(), shell=False, stdout=PIPE).stdout.read()
            vm_list = display_name_regex.findall(vm_listing_raw)
            if self.target_machine in vm_list:
                print "%s found on host: %s" % (self.target_machine, host)
                target_info = config_file_regex.findall(vm_listing_raw)
                target_info.insert(0, host)
        if len(target_info) < 2:
            return None
        else:
            return target_info

    # Returns true or false if the machine has snap
    def has_snapshots(self, vm_host, vm_config):
        check_snapshot_cmd = "%s -H %s -h %s -U %s -P %s %s hassnapshot" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config)
        try:
            snapshot_result = Popen(check_snapshot_cmd.split(), shell=False, stdout=PIPE).stdout.read()
            snapshot_len = "".join(re.split('\s', snapshot_result)[-1:])
            if snapshot_len > 0:
                return True
            else:
                return False
        except:
            print "Error retrieving machine status.\n"

    # Retrieves the vm state
    def get_state(self, vm_host, vm_config):
        getstate_machine_cmd = "%s -H %s -h %s -U %s -P %s %s getstate" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config)
        try:
            print "Retrieving machine state."
            call(getstate_machine_cmd.split(), shell=False)
        except CalledProcessError as e:
            print "Error retrieving machine state.\n" + str(e)

    # Reverts to the last snapshot
    def revert_snapshot(self, vm_host, vm_config):
        revert_snapshot_cmd = "%s -H %s -h %s -U %s -P %s %s revertsnapshot" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config)
        start_machine_cmd = "%s -H %s -h %s -U %s -P %s %s start" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config)
        if self.has_snapshots(vm_host, vm_config):
            try:
                print "Reverting snapshot."
                with open("/dev/null", "w") as devnull:
                    call(revert_snapshot_cmd.split(), shell=False, stdout=devnull)
                    print "Starting VM."
                    call(start_machine_cmd.split(), shell=False, stdout=devnull)
            except CalledProcessError as e:
                print "Error reverting snapshot.\n" + str(e)
        else:
            print "The target machine has no snapshots."

    # Takes a snapshot of a machine with the following additional parameters
    # snap_name: the snapshot name
    # snap_desc: a description for the snapshot
    # quiesc: if set to 1, the vm is powered on when snapshot is taken, and if vmware
    #   tools are installed, special file system sauce is applied.
    # snap_memory: takes a snapshot with memory. Takes more time.
    def take_snapshot(self, vm_host, vm_config, snap_name, snap_desc, quiesc, snap_memory):
        snapshot_cmd = "%s -H %s -h %s -U %s -P %s %s createsnapshot \"%s\" \"%s\" %s %s" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config,
             snap_name, snap_desc, quiesc, snap_memory)
        try:
            call(snapshot_cmd, shell=True)
        except CalledProcessError as e:
            print "Error creating snapshot.\n" + str(e)

    # This will remove all snapshots!!!
    def remove_snapshots(self, vm_host, vm_config):
        remove_snapshots_cmd = "%s -H %s -h %s -U %s -P %s %s removesnapshots" % \
            (self.vmware_cmd, self.vcenter_host, vm_host, self.vcenter_user, self.vcenter_pass, vm_config)
        try:
            call(remove_snapshots_cmd.split(), shell=False)
        except CalledProcessError as e:
            print "Error removing snapshots.\n" + str(e)
