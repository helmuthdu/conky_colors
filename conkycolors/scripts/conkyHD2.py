#!/usr/bin/env python
from os.path import normpath, basename, ismount
import subprocess

devices = subprocess.Popen(["lsblk | awk '{print $7}' | grep /"], shell=True, stdout=subprocess.PIPE,)

print ("${voffset 4}")

for device in devices.stdout:
    device = device.rstrip().decode("utf-8")
    if (ismount(device)):
        if (device is "/"):
            devicename="Root"
        else:
            devicename = basename(normpath(device)).capitalize()

        # start calculation dec value (for the pie chart symbol)
        statb = subprocess.Popen("stat -f -c %b "+device+"", shell=True, stdout=subprocess.PIPE,)
        statb_value = statb.communicate()[0]
        statf = subprocess.Popen("stat -f -c %f "+device+"", shell=True, stdout=subprocess.PIPE,)
        statf_value = statf.communicate()[0]
        total = int(statb_value)
        used = total - int(statf_value)
        dec = int((((used * 100) / total) + 5) / 10)
        if dec > 9:
            icon = "0"
        elif dec < 1:
            icon = "A"
        else:
            icon = str(dec)
        # end calculation dec

        print ("${voffset -6}${color0}${font Pie charts for maps:size=14}"+icon+"${font}${color}${offset 9}${voffset -5}"+devicename+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc "+device+"}%${color} ${alignr}${color2}${fs_free "+device+"}${color}${font}\n")

print ("${voffset -10}")
