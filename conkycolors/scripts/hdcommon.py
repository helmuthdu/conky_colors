#!/usr/bin/env python3

import os
from os.path import normpath, basename, ismount
from subprocess import Popen, PIPE

def get_partitions():
    p_lsblk = Popen(['lsblk', '-o', 'MOUNTPOINTS'], stdout=PIPE)
    output = p_lsblk.communicate()[0]
    for line in output.splitlines():
        device = line.rstrip().decode('utf-8')
        if not ismount(device):
            continue
        if device.startswith(('/snap/', '/var/lib/docker/btrfs', '/boot/efi', '/run/timeshift', '/tmp/apt-btrfs-snapshot', '/usr/lib/live/mount')):
            continue
        if (device == "/"):
            yield device, "Root"
        else:
            yield device, basename(normpath(device)).capitalize()

def get_pie_chart_icon(device):
    stat = os.statvfs(device)
    total = stat.f_blocks
    free = stat.f_bfree
    used = total - free
    dec = int((((used * 100) / total) + 5) / 10)
    if dec > 9:
        return "0"
    if dec < 1:
        return "A"
    return str(dec)
