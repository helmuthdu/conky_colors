#!/usr/bin/env python3

import os
from os.path import normpath, basename, ismount
from subprocess import Popen, PIPE

def get_partitions():
    p_lsblk = Popen(['lsblk'], stdout=PIPE)
    p_awk = Popen(['awk', '{print $7}'], stdin=p_lsblk.stdout, stdout=PIPE)
    p_grep = Popen(['grep', '/'], stdin=p_awk.stdout, stdout=PIPE)
    p_lsblk.stdout.close()
    p_awk.stdout.close()
    output = p_grep.communicate()[0]
    for line in output.splitlines():
        device = line.rstrip().decode('utf-8')
        if not ismount(device):
            continue
        if device.startswith('/snap/') or device == '/boot/efi':
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
