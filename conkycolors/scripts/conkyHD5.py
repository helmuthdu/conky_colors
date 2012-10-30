#!/usr/bin/env python2
import os

# root filesystem
print ("${voffset 0}${offset 0}${color0}${font Poky:size=14}y${font}${color}${offset 6}${voffset -7}Root: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /}%${color}${font}\n")
print ("${voffset -10}${offset 1}${color0}${fs_bar 4,18 /}${color}${offset 8}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /}${color}${font}\n")

# folder in /mnt
for device in os.listdir("/mnt/"):
	if (not device.startswith("cdrom")) and (os.path.ismount('/mnt/'+device)):
		print ("${voffset -10}${offset 0}${color0}${font Poky:size=14}y${font}${color}${offset 6}${voffset -7}"+device.capitalize()+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /mnt/"+device+"}%${color}${font}\n")
		print ("${voffset -10}${offset 1}${color0}${fs_bar 4,18 /mnt/"+device+"}${color}${offset 8}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /mnt/"+device+"}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /mnt/"+device+"}${color}${font}\n")
print ("${voffset -10}")
