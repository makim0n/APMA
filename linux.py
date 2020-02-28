#!/usr/bin/python2

import bs4
from urllib import urlopen
from vagrant_process import *

def linux_profile_parser(mem_dump):
    """
    :param mem_dump: Memory dump to analyze
    """
    tmp = ''
    ret = []
    f = open(mem_dump, 'rb')
    content = f.read()
    for line in content.splitlines():
        if "Linux version" in line:
            tmp += line
    # Try for Ubuntu linux
    try:
        #kernel_version = tmp.split(' ')[2]
        #linux_ver = 'Ubuntu %s' % tmp.split(' ')[9].split('~')[1][:5]
        ret.append(tmp.split(' ')[2])
        ret.append('Ubuntu %s' % tmp.split(' ')[9].split('~')[1][:5])
    except:
        pass

    # Try for Debian linux
    try:
        #kernel_version = tmp.split(' ')[2]
        #linux_ver = '%s %s' % (tmp.split(' ')[8][1:], tmp.split(' ')[6])
        ret.append(tmp.split(' ')[2])
        ret.append('%s %s' % (tmp.split(' ')[8][1:], tmp.split(' ')[6]))
    except:
        pass

    #print("Kernel version: %s" % kernel_version)
    #print("Linux version: %s" % linux_ver)
    print("Kernel version: %s" % ret[0])
    print("Linux version: %s" % ret[1])

    return ret

def box_url(linux_ver):
    fp = urlopen("https://app.vagrantup.com/boxes/search?sort=downloads&provider=virtualbox&q=%s" % linux_ver)
    html = fp.read()
    fp.close()

    soup = bs4.BeautifulSoup(html, "lxml")
    url = "https://app.vagrantup.com%s" % str(soup.find("a", {"class": "list-group-item"})).split('"')[3]

    return url

def vagrant_env(out_dir, linux_version, url):
    vagrant_init(out_dir, linux_version, url)