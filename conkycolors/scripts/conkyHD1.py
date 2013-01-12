#!/usr/bin/env python2
import os

# root filesystem
print ("${voffset 2}${offset 0}${color0}${font ConkyColors:size=15}i${font}${color}${offset 6}${voffset -10}Root: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /}%${color}${font}\n")
print ("${voffset -10}${offset 1}${color0}${fs_bar 4,17 /}${color}${offset 10}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /}${color}${font}\n")

# /home folder (if its a separate mount point)
if os.path.ismount("/home"):
	print ("${voffset -10}${offset 0}${color0}${font ConkyColors:size=15}i${font}${color}${offset 6}${voffset -10}Home: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /home}%${color}${font}\n")
	print ("${voffset -10}${offset 1}${color0}${fs_bar 4,17 /home}${color}${offset 10}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /home}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /home}${color}${font}\n")

# folder in /media
for device in os.listdir("/media/"):
	if (not device.startswith("cdrom")) and (os.path.ismount('/media/'+device)):
		print ("${voffset -10}${offset 0}${color0}${font ConkyColors:size=15}i${font}${color}${offset 6}${voffset -10}"+device.capitalize()+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /media/"+device+"}%${color}${font}\n")
		print ("${voffset -10}${offset 1}${color0}${fs_bar 4,17 /media/"+device+"}${color}${offset 10}${voffset -2}F: ${font Ubuntu:style=Bold:size=8}${color2}${fs_free /media/"+device+"}${color}${font} U: ${font Ubuntu:style=Bold:size=8}${color2}${fs_used /media/"+device+"}${color}${font}\n")
print ("${voffset -10}")
