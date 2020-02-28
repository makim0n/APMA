#!/usr/bin/python2

from fdisk import *
import os
import shutil


def offset(dump):
    """
    :param dump: Name of disk dump
    :return: Disk offset
    """
    f = open(dump, "rb")
    mbr = MBR()
    data = f.read(len(mbr))
    mbr.unpack(data)
    part_offset = mbr.partitions[0].start_sect
    f.close()

    return part_offset * 512

def bitlocker_key(path_output):
    """
    :param path_output: Path to output directory
    :return: Return tweak key formatted for bdemount
    """
    f = open("%s/cmd_win/bitlocker.txt" % path_output, "r")
    array = f.read().split('\n')
    fvek = array[3].split(':')[1].strip()
    tweak = array[4].split(':')[1].strip()
    f.close()

    return '%s:%s' % (fvek, tweak)

def bitlocker_vol_mount(dump, path_bde, offset, key, mnt_bde, path_output):
    """
    :param dump: Name of the disk dump
    :param path_bde:
    :param offset: Disk offset (block size * starting byte)
    :param key: Bitlocker keys from "bitlocker_key" function
    :param mnt_bde: Mount point for decrypt partition
    :param path_output: Path to output directory
    """
    os.system('bdemount -k %s -o %s %s %s' % (key, offset, dump, path_bde))
    decrypt_vol = os.listdir("%s/bde" % path_output)[0]
    new_path = os.path.join("%s/bde" % path_output, decrypt_vol)
    shutil.copyfile(new_path, "%s/bde1" % path_output)
    decrypt_vol_path = os.path.join(path_output, decrypt_vol)
    os.system('mount %s %s' % (decrypt_vol_path, mnt_bde))
    os.system('tree .')
