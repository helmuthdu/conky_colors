#!/usr/bin/env python
import os

# root filesystem
print ("${voffset -1}${color0}${font Poky:size=16}H${font}${color}${goto 32}${voffset -9}Root: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /}%${color}${font} ${alignr}${color2}${font Ubuntu:style=Bold:size=8}${fs_free /}${color}${font}\n")
# /home folder (if its a separate mount point)
if os.path.ismount("/home"):
	print ("${voffset -10}${goto 32}Home: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /home}%${color}${font} ${alignr}${font Ubuntu:style=Bold:size=8}${color2}${fs_free /home}${color}${font}\n")

# folder in /media
for device in os.listdir("/media/"):
	if (not device.startswith("cdrom")) and (os.path.ismount('/media/'+device)):
		print ("${voffset -10}${goto 32}"+device.capitalize()+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /media/"+device+"}%${color}${font} ${alignr}${font Ubuntu:style=Bold:size=8}${color2}${fs_free /media/"+device+"}${color}${font}\n")
print ("${voffset -10}")
