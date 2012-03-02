#!/usr/bin/env python
import os
import subprocess

# root filesystem
statb = subprocess.Popen("stat -f -c %b /", shell=True, stdout=subprocess.PIPE,)
statb_value = statb.communicate()[0]
statf = subprocess.Popen("stat -f -c %f /", shell=True, stdout=subprocess.PIPE,)
statf_value = statf.communicate()[0]
total = int(statb_value)
used = total - int(statf_value)
dec = (((used * 100) / total) + 5) / 10
if dec > 9:
	icon = "0"
elif dec < 1:
	icon = "A"
else:
	icon = str(dec)
print ("${voffset 2}${color0}${font Pie charts for maps:size=14}"+icon+"${font}${color}   ${voffset -5}Root: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /}%${color} ${alignr}${color2}${fs_free /}${color}${font}\n")

# /home folder (if its a separate mount point)
if os.path.ismount("/home"):
	# start calculation for the pie chart symbol (icon)
	statb = subprocess.Popen("stat -f -c %b /home", shell=True, stdout=subprocess.PIPE,)
	statb_value = statb.communicate()[0]
	statf = subprocess.Popen("stat -f -c %f /home", shell=True, stdout=subprocess.PIPE,)
	statf_value = statf.communicate()[0]
	total = int(statb_value)
	used = total - int(statf_value)
	dec = (((used * 100) / total) + 5) / 10
	if dec > 9:
		icon = "0"
	elif dec < 1:
		icon = "A"
	else:
		icon = str(dec)
	# end calculation icon
	print ("${voffset -6}${color0}${font Pie charts for maps:size=14}"+icon+"${font}${color}   ${voffset -5}Home: ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /home}%${color} ${alignr}${color2}${fs_free /home}${color}${font}\n")

# folder in /media
for device in os.listdir("/media/"):
	if (not device.startswith("cdrom")) and (os.path.ismount('/media/'+device)):
		# start calculation dec value (for the pie chart symbol)
		statb = subprocess.Popen('stat -f -c %b "/media/'+device+'"', shell=True, stdout=subprocess.PIPE,)
		statb_value = statb.communicate()[0]
		statf = subprocess.Popen('stat -f -c %f "/media/'+device+'"', shell=True, stdout=subprocess.PIPE,)
		statf_value = statf.communicate()[0]
		total = int(statb_value)
		used = total - int(statf_value)
		dec = (((used * 100) / total) + 5) / 10
		if dec > 9:
			icon = "0"
		elif dec < 1:
			icon = "A"
		else:
			icon = str(dec)
		# end calculation dec
		print ("${voffset -6}${color0}${font Pie charts for maps:size=14}"+icon+"${font}${color}   ${voffset -5}"+device.capitalize()+": ${font Ubuntu:style=Bold:size=8}${color1}${fs_free_perc /media/"+device+"}%${color} ${alignr}${color2}${fs_free /media/"+device+"}${color}${font}\n")
print ("${voffset -6}")
