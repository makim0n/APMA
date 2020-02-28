#!/usr/bin/python2

import vagrant
import os

def vagrant_init(out_dir, linux_version, url):
    new_path = os.path.join(out_dir, "vagrant")
    os.chdir(new_path)

    v = vagrant.Vagrant()
    v.init(linux_version, url)