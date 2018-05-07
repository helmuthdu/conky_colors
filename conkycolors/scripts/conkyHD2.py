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

    print("${voffset -6}${color0}${font Pie charts for maps:size=14}%(icon)s${font}${color}"
          "${offset 9}${voffset -5}%(devicename)s: ${font Ubuntu:style=Bold:size=8}${color1}"
          "${fs_free_perc %(device)s}%%${color} ${alignr}${color2}${fs_free %(device)s}${color}${font}\n"
          % {'device': device, 'devicename': devicename, 'icon': icon})

print("${voffset -10}")
