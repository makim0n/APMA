#!/usr/bin/python2
# -*- coding: utf8 -*-

from bitlocker_mount import *
import volatility.conf as conf

config = conf.ConfObject()
import volatility.registry as registry
import volatility.debug as debug
import volatility.addrspace as addrspace
import volatility.commands as commands

registry.PluginImporter()
registry.register_global_options(config, addrspace.BaseAddressSpace)
registry.register_global_options(config, commands.Command)
debug.setup()
cmds = registry.get_plugin_classes(commands.Command, lower=True)


def init(memdump, dump_dir):
    """
    :param path: Path of the memory dump file
    """
    config.LOCATION = "file://%s" % memdump
    config.DUMP_DIR = "%s/dump_dir" % dump_dir


def profil():
    """
    :return: Return the Windows profile
    """
    command = cmds["imageinfo"](config)
    x = command.calculate()  # Récupération du générateur
    config.PROFILE = x.next()[2].split(',')[0]  # Récupération du profil Windows

def vol_function(name, path):
    """
    :param name: Volatility plugin name
    :param path: Path to output directory
    """
    command = cmds[name](config)
    data = command.calculate()
    new_path = os.path.join(path, "cmd_win/%s.txt" % name)
    f = open(new_path, "w+")
    command.render_text(f, data)
    f.close()


def windows_bunch_cmds(output):
    """
    :param output: Path to output directory
    """
    i = 0
    vol_cmd = ["pstree", "psxview", "dlllist", "cmdscan", "consoles", "envars", "iehistory", "driverscan", "filescan",
               "symlinkscan", "netscan", "hivescan", "hivelist", "hashdump", "clipboard", "desktops", "editbox",
               "eventhooks", "messagehooks", "screenshot", "bitlocker", "mftparser"]
    for cmd in vol_cmd:
        i += 1
        try:
            vol_function(cmd, output)
            print("[+] %s command executed (%s/%s)" % (cmd, i, len(vol_cmd)))
        except:
            print("[-] %s command failed (%s/%s)" % (cmd, i, len(vol_cmd)))

def bitlocker_mount(dump, path_output, mnt_bde):
    """
    :param dump: Name of the disk dump
    :param path_output: Path to output directory
    :param mnt_bde:
    """
    offset_part = offset(dump)
    key = bitlocker_key(path_output)
    bitlocker_vol_mount(dump, "%s/bde" % path_output, offset_part, key, mnt_bde, path_output)

