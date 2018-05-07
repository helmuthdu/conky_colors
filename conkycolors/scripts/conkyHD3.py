#!/usr/bin/env python3

import os
import sys
from os.path import abspath, dirname

directory = dirname(abspath(__file__))
sys.path.insert(0, directory)

from hdcommon import get_partitions, get_pie_chart_icon


print ("${voffset 4}")

for device, devicename in get_partitions():
    icon = get_pie_chart_icon(device)
    var_map = {'device': device, 'devicename': devicename, 'icon': icon}

    print("${voffset -10}${color0}${font Pie charts for maps:size=15}%(icon)s"
          "${font}${color}${offset 9}${voffset -9}%(devicename)s: "
          "${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc %(device)s}%%${color}${font}\n" % var_map)
    print("${voffset -10}${offset 29}F: ${font Ubuntu:style=Bold:size=8}${color2}"
          "${fs_free %(device)s}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}"
          "${fs_used %(device)s}${color}${font}\n" % var_map)

print("${voffset -10}")
