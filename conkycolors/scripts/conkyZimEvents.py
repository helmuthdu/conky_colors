#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################

from time import localtime, strftime
import calendar
import os

''' Settings '''
HOME = os.path.expanduser('~')
CAL_PATH =  HOME + "/.zim/Calendar"

year = int(strftime("%Y", localtime()))
month = int(strftime("%m", localtime()))
today = int(strftime("%d", localtime()))

dir = os.path.join(CAL_PATH, "%04d/%02d" % (year, month))
num_events = 0

if os.path.isdir(dir):
    for day in range(today, calendar.monthrange(int(year), int(month))[1]+1):
        day_path = "%s/%02d.txt" % (dir, day)
        if os.path.exists(day_path):
            with open(day_path) as event:
                lines = event.readlines()
                print "${color0}" + lines[4].strip('= \n') + "${color}"
                for line in lines[6:]:
                    print " ", line,
                num_events=num_events+1
                if num_events >= 5:
                    break

if num_events < 5:
    if month == 12:
        month = 1
        year = year+1
    else:
        month = month+1
    dir = os.path.join(CAL_PATH, "%04d/%02d" % (year, month))
    day = 1
    if os.path.isdir(dir):
        for day in range(1, calendar.monthrange(int(year), int(month))[1]+1):
            day_path = "%s/%02d.txt" % (dir, day)
            if os.path.exists(day_path):
                with open(day_path) as event:
                    lines = event.readlines()
                    print "${color0}" + lines[4].strip('= \n') + "${color}"
                    for line in lines[6:]:
                        if line != ("" or "\n"):
                            print " ", line[:24],
                    num_events=num_events+1
                    if num_events >= 5:
                        break
