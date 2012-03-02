#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################

from time import localtime, strftime
import calendar
import os

''' Settings '''
HOME = os.path.expanduser('~')
CAL_PATH =  HOME + "/.zim/Calendar"

year = strftime("%Y", localtime())
month = strftime("%m", localtime())
today = int(strftime("%d", localtime()))
fday = calendar.weekday(int(year), int(month), 1)

dir = os.path.join(CAL_PATH, year + "/" + month)

# Calendar
weekName = os.system('cal | sed \'2!d\'')
for day in range(1,calendar.monthrange(int(year), int(month))[1]+1):
    daystr = "%02d" % day
    if day is today:
        daystr = "${color2}" + daystr + "${color}"
    if os.path.exists(os.path.join(dir, str(day) + ".txt")):
        daystr = "${color0}" + daystr + "${color}"
    print daystr,
    if ((fday+day) % 7) == 0:
        print
