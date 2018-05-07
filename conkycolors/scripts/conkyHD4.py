#!/usr/bin/env python3

import os
import sys
from os.path import abspath, dirname

directory = dirname(abspath(__file__))
sys.path.insert(0, directory)

from hdcommon import get_partitions


print("${voffset 4}${color0}${font ConkyColors:size=18}h${font}${color}${voffset 5}${offset -21}${diskiograph 4,17}${voffset -32}\n")

for device, devicename in get_partitions():
    print("${voffset -10}${goto 32}%(devicename)s: ${font Ubuntu:style=Bold:size=8}${color1}"
          "${fs_free_perc %(device)s}%%${color}${font} ${alignr}${font Ubuntu:style=Bold:size=8}"
          "${color2}${fs_free %(device)s}${color}${font}\n"
          % {'device': device, 'devicename': devicename})

print("${voffset -10}")
