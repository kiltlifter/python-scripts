#!/usr/bin/python
__author__ = 'sdouglas'


import sys, os


def dir_file(dir):
    with open(dir+".txt", 'w') as f:
        list_files_command = "ls -aLR1 %s" % dir
        f.writelines(os.popen(list_files_command))


def parse_file(dir):
    lines = (line.rstrip('\n') for line in open(dir+".txt"))
    with open(dir+"-spec.txt", 'w') as f:
        current_dir = ""
        for index in lines:
            if index == "." or index == "..":
                continue
            if  len(index) < 1:
                print "\n"
                f.writelines("\n")
            elif index[-1:] == ":":
                new_index = index[:-1]
                split_index = new_index.split("/")
                split_index2 = split_index
                split_index2[0] = "%{_datadir}/%{_shortname}"
                current_dir = '/'.join(split_index2)
                split_index[0] = "%dir %{_datadir}/%{_shortname}"
                new_line = '/'.join(split_index)
                print new_line
                f.writelines(new_line+"\n")
            else:
                file_line = "  %s/%s" % (current_dir, index)
                print file_line
                f.writelines(file_line+"\n")

    lines.close()


def main():
    if len(sys.argv) > 2 or len(sys.argv) < 1:
        print "Proper usage: python list-contents.py target-dir/"
    target_dir = sys.argv[1]
    dir_file(target_dir)
    parse_file(target_dir)

if __name__ == '__main__':
    main()