#!/usr/bin/env python
from os.path import normpath, basename, ismount
import subprocess

devices = subprocess.Popen(["lsblk | awk '{print $7}' | grep /"], shell=True, stdout=subprocess.PIPE,)

print ("${voffset 4}${color0}${font ConkyColors:size=18}h${font}${color}${voffset 5}${offset -21}${diskiograph 4,17}${voffset -32}\n")

for device in devices.stdout:
    device = device.rstrip().decode("utf-8")
    if device == u'/boot/efi':
        continue
    if (ismount(device)):
        if (device == u"/"):
            devicename="Root"
        else:
            devicename = basename(normpath(device)).capitalize()

        print ("${voffset -10}${goto 32}"+devicename+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc "+device+"}%${color}${font} ${alignr}${font Ubuntu:style=Bold:size=8}${color2}${fs_free "+device+"}${color}${font}\n")

print ("${voffset -10}")
