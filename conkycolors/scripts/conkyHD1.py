#!/usr/bin/env python3

import sys
from os.path import abspath, dirname

directory = dirname(abspath(__file__))
sys.path.insert(0, directory)

from hdcommon import get_partitions


print("${voffset 4}")

for device, devicename in get_partitions():
    var_map = {'device': device, 'devicename': devicename}
    print("${voffset -10}${offset 0}${color0}${font ConkyColors:size=15}i${font}${color}${offset 6}"
          "${voffset -10}%(devicename)s: ${font Ubuntu:style=Bold:size=8}${color1}"
          "${fs_free_perc %(device)s}%%${color}${font}\n" % var_map)
    print("${voffset -10}${offset 1}${color0}${fs_bar 4,17 %(device)s}${color}${offset 10}"
          "${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free %(device)s}${color}"
          "${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used %(device)s}${color}${font}\n" % var_map)

print("${voffset -10}")
