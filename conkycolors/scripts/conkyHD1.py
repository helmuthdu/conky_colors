#!/usr/bin/env python
from os.path import normpath, basename
import subprocess

devices = subprocess.Popen(["lsblk | awk '{print $7}' | grep /"], shell=True, stdout=subprocess.PIPE)

print ("${voffset 4}")

for device in devices.stdout:
    device = device.rstrip().decode("utf-8")
    if (device is "/"):
        devicename="Root"
    else:
        devicename = basename(normpath(device)).capitalize()

    print ("${voffset -10}${offset 0}${color0}${font ConkyColors:size=15}i${font}${color}${offset 6}${voffset -10}"+devicename+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc "+device+"}%${color}${font}\n")
    print ("${voffset -10}${offset 1}${color0}${fs_bar 4,17 "+device+"}${color}${offset 10}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free "+device+"}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used "+device+"}${color}${font}\n")

print ("${voffset -10}")
