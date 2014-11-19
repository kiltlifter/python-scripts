#!/usr/bin/python
__author__ = 'sdouglas'


import sys, os


def find_dirs(dir):
    if dir[-1:] == "/":
        dir = dir[:-1]
    with open(dir+".txt", 'w') as f:
        list_files_command = "find %s -type d -print" % dir
        f.writelines(os.popen(list_files_command))


def traverse_dirs(target):
    if target[-1:] == "/":
        target = target[:-1]
    with open(target+".txt", 'r') as f:
        contents = f.readlines()
        with open("final-file.txt", 'w') as e:
            for line in contents:
                try:
                    file_command = "find %s -type f -print > /dev/null 2>&1" % line
                    e.writelines(os.popen(file_command))
                except Exception:
                    print line




def parse_file(dir):
    if dir[-1:] == "/":
        dir = dir[:-1]
    lines = (line.rstrip('\n') for line in open("final-file.txt"))
    with open(dir+"-spec.txt", 'w') as f:
        current_dir = ""
        for index in lines:
            if os.path.isdir(index):
                split_index = index.split("/")
                split_index.remove(dir)
                current_dir = '/'.join(split_index)
                spec_file_dir = "%dir %{_openam_webapp_dir}"
                new_line = "%s/%s" % (spec_file_dir,current_dir)
                print new_line
                f.writelines(new_line+"\n")
                """
                new_index = index[:-1]
                split_index = new_index.split("/")
                split_index2 = split_index
                split_index2[0] = "%{_datadir}/%{_shortname}"
                current_dir = '/'.join(split_index2)
                split_index[0] = "%dir %{_datadir}/%{_shortname}"
                new_line = '/'.join(split_index)
                print new_line
                f.writelines(new_line+"\n")
                """
            else:
                split_file = index.split('/')
                split_file.remove(dir)
                current_file = '/'.join(split_file)
                spec_file_format = "%{_openam_webapp_dir}"
                file_line = "   %s/%s" % (spec_file_format,current_file)
                print file_line
                f.writelines(file_line+"\n")
                """
                file_line = "  %s/%s" % (current_dir, index)
                print file_line
                f.writelines(file_line+"\n")
                """

    lines.close()


def main():
    if len(sys.argv) > 2 or len(sys.argv) < 1:
        print "Proper usage: python list-contents.py target-dir/"
    target_dir = sys.argv[1]
    find_dirs(target_dir)
    traverse_dirs(target_dir)
    parse_file(target_dir)
    #parse_file(target_dir)

if __name__ == '__main__':
    main()