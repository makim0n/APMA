#!/usr/bin/python2
import argparse
import re
from windows import *
from bitlocker_mount import *
from linux import *


def arg_parser():
    """
    :return: Return parsed args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plugins", type=str, help="Path to plugin volatility directory")
    parser.add_argument("FILE", type=str, help="Path to memory dump")
    parser.add_argument("-o", "--output", type=str, help="Output directory", default="output")
    parser.add_argument("-d", "--disk", type=str, help="Path to disk dump")
    args = parser.parse_args()
    return args


def tree(directory):
    """
    :param directory: Output directory name (default is "output")
    """
    # Create output directory and audit.txt file
    try:
        os.mkdir(directory)
        os.mkdir("%s/cmd_win" % directory)
        os.mkdir("%s/dump_dir" % directory)
        os.mkdir("%s/vagrant" % directory)
        os.mknod(directory + "/audit.txt")
    except:
        print('[!] Output directory already exists.')
        exit()


def os_detection(dump):
    """
    :param dump: Name of the memory dump file
    :return: Return OS type, Linux or Windows
    """
    f = open(dump, 'rb')
    content = f.read()
    if re.search('Linux version', str(content)):
        osType = "Linux"
    else:
        osType = "Windows"
    f.close()
    return osType


def audit_filling(path, content):
    """
    :param path: Path to audit.txt file
    :param content: Data to append
    """
    f = open(path, 'a')
    f.write(content + '\n')
    f.close()


if __name__ == "__main__":
    args = arg_parser()
    tree(args.output)
    init(args.FILE, args.output)
    os_type = os_detection(args.FILE)
    audit_filling("%s/audit.txt" % args.output, "[+] OS Type: %s" % os_type)
    if os_type == "Windows":
        i = 0
        profil()
        audit_filling("%s/audit.txt" % args.output, "[+] Profile: %s" % config.PROFILE)
        windows_bunch_cmds(args.output)

        if args.disk:
            f = open(args.disk, 'rb')
            if re.search('-FVE-FS-', f.read()):
                print("[+] Bitlocker disk dump detected!")
                os.mkdir("%s/bde" % args.output)
                os.mkdir("%s/mnt" % args.output)
                bitlocker_mount(args.disk, args.output, "%s/mnt" % args.output)
            else:
                print('[-] Not a bitlocker disk dump.')
    else:
        info = []
        info = linux_profile_parser(args.FILE)
        url = box_url(info[1])
        vagrant_env(args.output, info[1], url)
