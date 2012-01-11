#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyGoogleCalendar.py is a simple python script to output google calendar
# event details in conky.
#
# Author: Kaivalagi
# Created: 22/06/2008

from datetime import datetime, date, timedelta
from dateutil.relativedelta import *
from optparse import OptionParser
from xml.dom import minidom
from keyring import get_password
import socket
import gdata.calendar.service
import sys
import locale
import re
import textwrap
import urllib
import codecs
import traceback
import os

class CalendarData:

    def __init__(self, title):
        self.title = title

class CalendarEventData:

    def __init__(self, title, starttime, endtime, location, description, who=None):
        self.title = title
        self.starttime = starttime
        self.endtime = endtime
        self.location = location
        self.description = description
        self.who = who

    def __cmp__(self, other):
        return cmp(self.starttime, other.starttime)

    def __str__(self):
        return str(self.starttime)

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-u","--username", dest="username", type="string", metavar="USERNAME", help=u"Username for login into Google Calendar, this will normally be your gmail account")
        self.parser.add_option("-p","--password",dest="password", type="string", metavar="PASSWORD", help=u"Password to login with, if not set the username is used to fetch a 'conky' password from the keyring")
        self.parser.add_option("-r","--requestCalendarNames",dest="requestedCalendars", type="string", metavar="TEXT", help=u"Define a list of calendars to request event data for, calendar names should be separated by semi-colons \";\". For example --requestCalendarNames=\"cal1;cal2;other cal\" If not set all calendar data will be returned.")
        self.parser.add_option("-d","--daysahead",dest="daysahead", default=7, type="int", metavar="NUMBER", help=u"[default: %default] Define the number of days ahead you wish to retrieve calendar entries for, starting from today.")
        self.parser.add_option("-s","--startdate",dest="startdate", type="string", metavar="DATE", help=u"Define the start date to retrieve calendar events. In the form '2007-12-01'")
        self.parser.add_option("-e","--enddate",dest="enddate", type="string", metavar="DATE", help=u"Define the end date to retrieve calendar events, must be supplied if --startdate supplied. In the form '2007-12-01'")
        self.parser.add_option("-a","--allevents",dest="allevents", default=False, action="store_true", help=u"Retrieve all calendar events")
        self.parser.add_option("-w","--wordsearch",dest="wordsearch", type="string", metavar="TEXT", help=u"Define the text to search calendar entries with.")
        self.parser.add_option("-l","--limit",dest="limit", default=0, type="int", metavar="NUMBER", help=u"[default: %default] Define the maximum number of calendar events to display, zero means no limit.")
        self.parser.add_option("-t","--template",dest="template", type="string", metavar="FILE", help=u"Template file determining the format for each event. Use the following placeholders: [title], [starttime], [endtime], [completetime], [duration], [location], [description], [who]. Ensure only one placeholder per line, as the whole line is removed if no data for that placeholder exists.")
        self.parser.add_option("-f","--dateformat",dest="dateformat", default=None, type="string", metavar="\"DATEFORMAT\"", help=u"If used this overrides the default date formatting. The values to use are standard formatting strings e.g. Weekday=%a, Day=%d, Month=%m, Year=%y. For an output like \"Thu 15/10/2008\" you would require --dateformat=\"%a %d/%m/%y\", to have no date you would require --dateformat=\"\"")
        self.parser.add_option("-F","--timeformat",dest="timeformat", default=None, type="string", metavar="\"TIMEFORMAT\"", help=u"If used this overrides the default time formatting. The values to use are standard formatting strings e.g. Hours (12hr)=%l, Hours (24hr)=%H, Minutes=%M, Seconds=%S, AM/PM=%P. For an output like \"05:22 PM\" you would require --timeformat=\"%l:%M %P\", --timeformat=\"\" is not supported, default locale settings are used")
        self.parser.add_option("-i","--indent",dest="indent", default=0, type="int", metavar="NUMBER", help=u"[default: %default] Define the number of spaces to indent the output (excludes template based output)")
        self.parser.add_option("-m","--maxwidth",dest="maxwidth", default=40, type="int", metavar="NUMBER", help=u"[default: %default] Define the number of characters to output per line")
        self.parser.add_option("-n","--nowho",dest="nowho", default=False, action="store_true", help=u"Hides who is attending the events (excludes template based output)")
        self.parser.add_option("-c","--connectiontimeout",dest="connectiontimeout", type="int", default=30, metavar="NUMBER", help=u"[default: %default] Define the number of seconds before a connection timeout can occur.")
        self.parser.add_option("-v","--verbose",dest="verbose", default=False, action="store_true", help=u"Request verbose output, no a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class GoogleCalendarInfo:

    dateformat=""
    timeformat=""
    options = None

    requestedCalendars = []
    requiredCalendars = []
    feedPrefix    = 'https?://www.google.com/calendar/feeds/'
    ACCESS_ALL         = 'all'      # non-google access level
    ACCESS_DEFAULT     = 'default'  # non-google access level
    ACCESS_NONE        = 'none'
    ACCESS_OWNER       = 'owner'
    ACCESS_EDITOR      = 'editor'
    ACCESS_CONTRIBUTOR = 'contributor'
    ACCESS_READ        = 'read'
    ACCESS_FREEBUSY    = 'freebusy'

    ################ GOOGLE CALENDAR FUNCTIONS ################################
    def __init__(self, options):

        try:
            # store options for use throughout the class
            self.options = options

            # obtain a password from the keyring if none is set
            if self.options.password == None:
                self.logInfo("Attempting to obtain a password through the conky keyring as none was provided")
                
                try:
                    password = get_password("conky", self.options.username)
                except Exception, e:
                    self.logError("Failed to retrieve password from keyring:" + traceback.format_exc())
                
                if password == None:
                    self.logError("No password was found in the conky keyring")
                else:
                    self.options.password = password
                 
                
            self.logInfo("Initialising google calendar connection...")

            socket.setdefaulttimeout(self.options.connectiontimeout)

            self.cal_client = gdata.calendar.service.CalendarService()
            self.cal_client.email = self.options.username
            self.cal_client.password = self.options.password
            self.cal_client.source = 'conkyGoogleCalendar'
            self.cal_client.ProgrammaticLogin()

            # load the format for date and time to use
            self.getDatetimeFormat(self.options.dateformat, self.options.timeformat)

            # prepare calendar list to use for event retrieval
            self.getCalendarList()

        except Exception,e:
            self.logError("GoogleCalendarEngine Initialisation:Unexpected error:" + traceback.format_exc())

    def getDatetimeFormat(self,dateformat=None,timeformat=None):

        try:

            # get locale defaults for output
            locale.setlocale(locale.LC_ALL,'')

            # format date based on format setting
            if dateformat == None:
                self.dateformat = "%a "+locale.nl_langinfo(locale.D_FMT)
            elif dateformat == "":
                self.dateformat = ""
            else:
                self.dateformat = dateformat

            # format time based on format setting
            if timeformat == None or timeformat == "":
                self.timeformat = locale.nl_langinfo(locale.T_FMT)
            else:
                self.timeformat = timeformat

        except Exception,e:
            self.logError("getDatetimeFormat:Unexpected error:" + traceback.format_exc())

    def getCalendarList(self):

        self.logInfo("Preparing google calendar list...")

        # prepare calendar list to retrieve
        if self.options.requestedCalendars != None:
            self.requestedCalendars = self.options.requestedCalendars.split(";")

        # get the list of calendars from google
        calendars = self.cal_client.GetAllCalendarsFeed()

        order = { self.ACCESS_OWNER       : 1,
                  self.ACCESS_EDITOR      : 2,
                  self.ACCESS_CONTRIBUTOR : 3,
                  self.ACCESS_READ        : 4,
                  self.ACCESS_FREEBUSY    : 5,
                  self.ACCESS_NONE        : 6 }

        calendars.entry.sort(lambda x, y:
                                cmp(order[x.access_level.value],
                                    order[y.access_level.value]))

        # clear the list
        self.requiredCalendars = []

        for cal in calendars.entry:

            cal.gcalcli_altLink = cal.GetAlternateLink().href
            match = re.match('^' + self.feedPrefix + '(.*?)/(.*?)/(.*)$',cal.gcalcli_altLink)
            cal.username    = urllib.unquote(match.group(1))
            cal.visibility  = urllib.unquote(match.group(2))
            cal.projection  = urllib.unquote(match.group(3))

            if len(self.requestedCalendars):

                # get the calendar name, updating it if an override is found
                calendarName = cal.title.text
                doc = minidom.parseString(str(cal))
                overrideName = doc.getElementsByTagNameNS(u'http://schemas.google.com/gCal/2005', 'overridename')
                if len(overrideName) > 0:
                    calendarName = overrideName[0].getAttribute("value")

                for rc in self.requestedCalendars:
                    if rc.lower() == calendarName.lower():
                        self.requiredCalendars.append(cal)
            else:
                self.requiredCalendars.append(cal)


    def getOwnedCalendars(self):

        try:

            self.logInfo("Fetching owned calendars...")

            feed = self.cal_client.GetOwnCalendarsFeed()

            calendarDataList = []

            for mycalendar in zip(xrange(len(feed.entry)), feed.entry):
                calendarData = CalendarData(mycalendar.title.text)
                calendarDataList.append(calendarData)

            return calendarDataList

        except Exception,e:
            self.logError("getOwnedCalendars:Unexpected error:" + traceback.format_exc())
            return []

    def getAllEvents(self):

        try:

            self.logInfo("Fetching all event data...")

            calendarDataEventList = []

            for cal in self.requiredCalendars:
                query = gdata.calendar.service.CalendarEventQuery(cal.username, cal.visibility, cal.projection)
                feed = self.cal_client.CalendarQuery(query)
                now = datetime.now()
                for i, event in zip(xrange(len(feed.entry)), feed.entry):
                    for j, when in zip(xrange(len(event.when)), event.when):
                        for k, where in zip(xrange(len(event.where)), event.where):
                            # if the event's end time is after now then add it!
                            if self.getDatetimeFromWhen(when.end_time) > now:
                                whoList = []
                                for l, who in zip(xrange(len(event.who)), event.who):
                                    whoList.append(who.email)
                                if len(whoList) == 0:
                                    whoList = None
                                calendarDataEvent = CalendarEventData(event.title.text, when.start_time, when.end_time, where.value_string, event.content.text, whoList)
                                calendarDataEventList.append(calendarDataEvent)

            return calendarDataEventList

        except Exception,e:
            self.logError("getAllEvents:Unexpected error:" + traceback.format_exc())
            return []

    def getTextQueryEvents(self, text_query='Project'):

        try:

            self.logInfo("Fetching text queried event data using text query of \"%s\"..."%text_query)

            calendarDataEventList = []

            for cal in self.requiredCalendars:

                query = gdata.calendar.service.CalendarEventQuery(cal.username, cal.visibility, cal.projection, text_query)
                query.orderby = 'starttime'
                query.singleevents = 'true'
                feed = self.cal_client.CalendarQuery(query)
                now = datetime.now()
                for i, event in zip(xrange(len(feed.entry)), feed.entry):
                    for j, when in zip(xrange(len(event.when)), event.when):
                        for k, where in zip(xrange(len(event.where)), event.where):
                            # if the event's end time is after now then add it!
                            if self.getDatetimeFromWhen(when.end_time) > now:
                                whoList = []
                                for l, who in zip(xrange(len(event.who)), event.who):
                                    whoList.append(who.email)
                                if len(whoList) == 0:
                                    whoList = None
                                calendarDataEvent = CalendarEventData(event.title.text, when.start_time, when.end_time, where.value_string, event.content.text, whoList)
                                calendarDataEventList.append(calendarDataEvent)

            return calendarDataEventList

        except Exception,e:
            self.logError("getTextQueryEvents:Unexpected error:" + traceback.format_exc())
            return []

    def getDateRangedEvents(self, start_date='2007-01-01', end_date='2020-01-01'):

        try:

            self.logInfo("Fetching date ranged event data for dates between %s and %s..."%(start_date,end_date))

            calendarDataEventList = []

            for cal in self.requiredCalendars:

                query = gdata.calendar.service.CalendarEventQuery(cal.username, cal.visibility, cal.projection)
                query.start_min = start_date
                query.start_max = end_date
                query.orderby = 'starttime'
                query.singleevents = 'true'
                feed = self.cal_client.CalendarQuery(query)
                for i, event in zip(xrange(len(feed.entry)), feed.entry):
                    for j, when in zip(xrange(len(event.when)), event.when):
                        for k, where in zip(xrange(len(event.where)), event.where):
                            whoList = []
                            for l, who in zip(xrange(len(event.who)), event.who):
                                whoList.append(who.email)
                            if len(whoList) == 0:
                                whoList = None
                            calendarDataEvent = CalendarEventData(event.title.text, when.start_time, when.end_time, where.value_string, event.content.text, whoList)
                            calendarDataEventList.append(calendarDataEvent)

            return calendarDataEventList

        except Exception,e:
            self.logError("getDateRangedEvents:Unexpected error:" + traceback.format_exc())
            return []

    def getFutureEvents(self, days_ahead=7):

        try:

            self.logInfo("Fetching future event data, for the next %s days..."%days_ahead)

            calendarDataEventList = []

            for cal in self.requiredCalendars:

                query = gdata.calendar.service.CalendarEventQuery(cal.username, cal.visibility, cal.projection)
                query.start_min = str(date.today())
                query.start_max = str(date.today()+timedelta(days=days_ahead))
                query.orderby = 'starttime'
                query.singleevents = 'true'
                feed = self.cal_client.CalendarQuery(query)
                now = datetime.now()
                for i, event in zip(xrange(len(feed.entry)), feed.entry):
                    for j, when in zip(xrange(len(event.when)), event.when):
                        for k, where in zip(xrange(len(event.where)), event.where):
                            # if the event's end time is after now then add it!
                            if self.getDatetimeFromWhen(when.end_time) > now:
                                whoList = []
                                for l, who in zip(xrange(len(event.who)), event.who):
                                    whoList.append(who.email)
                                if len(whoList) == 0:
                                    whoList = None
                                calendarDataEvent = CalendarEventData(event.title.text, when.start_time, when.end_time, where.value_string, event.content.text, whoList)
                                calendarDataEventList.append(calendarDataEvent)

            return calendarDataEventList

        except Exception,e:
            self.logError("getFutureEvents:Unexpected error:" + traceback.format_exc())
            return []

    def getDuration(self, starttime, endtime):
        
        if endtime > starttime:
            rdelta = relativedelta(endtime, starttime)
        else:
            endtime = endtime + timedelta(days=+1)
            rdelta = relativedelta(endtime, starttime)

        output = u""
        
        if rdelta.days > 0:
            if rdelta.days == 1:
                suffix = " day "
            else:
                suffix = " days "

            output = output + str(rdelta.days) + suffix
                    
        if rdelta.hours > 0:
            if rdelta.hours == 1:
                suffix = " hr "
            else:
                suffix = " hrs "

            output = output + str(rdelta.hours) + suffix
            
        if rdelta.minutes > 0:
            if rdelta.minutes == 1:
                suffix = " min "
            else:
                suffix = " mins "

            output = output + str(rdelta.minutes) + suffix
        
        return output
        
    def getFormattedEventTimes(self, starttime, endtime):

        datematch = (datetime.strftime(starttime, self.dateformat) == datetime.strftime(endtime, self.dateformat))
        timematch = (datetime.strftime(starttime, self.timeformat) == datetime.strftime(endtime, self.timeformat))

        if datematch == True:
            if timematch == True:
                completetime = self.getDatetimeString(starttime)
                duration = ""
            else:
                completetime = "%s to %s"%(self.getDatetimeString(starttime), datetime.strftime(endtime, self.timeformat))
                duration = "for %s"%self.getDuration(starttime, endtime)
        else:
            if timematch == True:
                if starttime.hour == 0 and endtime.hour == 0 and (endtime - starttime == timedelta(days=1)):
                    completetime = datetime.strftime(starttime, self.dateformat)
                    duration = "for %s"%self.getDuration(starttime, endtime)                    
                else:
                    completetime = "%s to %s"%(self.getDatetimeString(starttime), datetime.strftime(endtime, self.dateformat))
                    duration = "for %s"%self.getDuration(starttime, endtime)
            else:
                completetime = "%s to %s"%(self.getDatetimeString(starttime), self.getDatetimeString(endtime))
                duration = "for %s"%self.getDuration(starttime, endtime)

        if starttime.hour == 0 and endtime.hour == 0:
            starttime = datetime.strftime(starttime, self.dateformat)
            endtime = datetime.strftime(endtime, self.dateformat)       
        else:
            starttime = self.getDatetimeString(starttime)
            endtime = self.getDatetimeString(endtime)
        
        return starttime, endtime, completetime, duration

    def getDatetimeString(self,whendatetime, format=None):

        try:

            # is this a datetime or just date field
            if whendatetime.year != 1900:
                dateandtime = True
            else:
                dateandtime = False
                
            if dateandtime == True:
                if self.dateformat == "":
                    whendatetime = whendatetime.strftime(self.timeformat)
                else:
                    whendatetime = whendatetime.strftime(self.dateformat + " " + self.timeformat)
            else:
                if self.dateformat == "": # if no formating but only required to show date we need then revert to default!
                    whendatetime = whendatetime.strftime(locale.nl_langinfo(locale.D_FMT))
                else:
                    whendatetime = whendatetime.strftime(self.dateformat)

            # remove excess space between date and time if necessary
            whendatetime = whendatetime.replace("  "," ")

            return whendatetime

        except Exception,e:
            self.logError("getDatetimeString:Unexpected error:" + traceback.format_exc)
            
    def getDatetimeFromWhen(self, when):

        try:

            # is this a datetime or just date field
            if len(when) > 10:
                dateandtime = True
            else:
                dateandtime = False

            # convert to datetime field
            if dateandtime == True:
                whendatetime = datetime.strptime(when[0:19], "%Y-%m-%dT%H:%M:%S")
            else:
                whendatetime = datetime.strptime(when[0:10], "%Y-%m-%d")

            return whendatetime

        except Exception,e:
            self.logError("getDatetimeFromWhen:Unexpected error:" + traceback.format_exc)
                        
    def removeLineByString(self,lines,string):

        # define list from multiple lines, to allow remove function
        lineslist = lines.split("\n")
        lineslistchanged = False

        for line in lineslist:
            if line.find(string) <> -1:
                lineslist.remove(line)
                lineslistchanged = True
                break

        if lineslistchanged == True:
            # rebuild lines string from updated list
            lines = "\n".join(lineslist)

        return lines

    def getSpaces(self,spaces):
        string = ""
        for i in range(0, spaces+1):
            string = string + " "
        return string

    def getWrappedText(self,text,width=40,indent=0):
        if len(text) > width:
            indentspace = "".ljust(indent)
            wrappedtext=""
            for line in textwrap.wrap(text,width=(width-indent),expand_tabs=False,replace_whitespace=False):
                wrappedtext = wrappedtext + line + "\n" + indentspace
            return wrappedtext.rstrip("\n ")
        else:
            return text

    def logInfo(self, text):
        if self.options.verbose == True:
            print >> sys.stdout, "INFO: " + text

        if self.options.infologfile != None:
            datetimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fileoutput = open(self.options.infologfile, "ab")
            fileoutput.write(datetimestamp+" INFO: "+text+"\n")
            fileoutput.close()

    def logError(self, text):
        print >> sys.stderr, "ERROR: " + text

        if self.options.errorlogfile != None:
            datetimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fileoutput = open(self.options.errorlogfile, "ab")
            fileoutput.write(datetimestamp+" ERROR: "+text+"\n")
            fileoutput.close()

    def getMadeSafeOutput(self, text):
        return text.replace("${exec","${!noexec!")

    def getOutputFromTemplate(self, template, title, starttime, endtime, location, description, who):

        try:

            output = template

            if title == None or title.strip() == "":
                output = self.removeLineByString(output,"[title]")
            else:
                output = output.replace("[title]",title)

            if location == None or location.strip() == "":
                output = self.removeLineByString(output,"[location]")
            else:
                output = output.replace("[location]",location)

            if description == None or description.strip() == "":
                output = self.removeLineByString(output,"[description]")
            else:
                output = output.replace("[description]",description)

            if who == None or who.strip() == "":
                output = self.removeLineByString(output,"[who]")
            else:
                #output = output.replace("[who]",";".join(who))
                output = output.replace("[who]",who)

            starttime, endtime, completetime, duration = self.getFormattedEventTimes(starttime, endtime)

            output = output.replace("[starttime]",starttime)
            output = output.replace("[endtime]",endtime)
            
            if output.find("[completetime]") != -1:
                output = output.replace("[completetime]",completetime)
                
            if output.find("[duration]") != -1:
                output = output.replace("[duration]",duration)

            # get rid of any excess crlf's and add just one
            #output = output.rstrip(" \n")
            #output = output + "\n"

            return output

        except Exception,e:
            self.logError("getOutputFromTemplate:Unexpected error:" + traceback.format_exc())
            return ""
        
    def writeOutput(self):

        try:

            ################ GOOGLE CALENDAR DATA RETRIEVAL #########################

            # determine the required query and run it
            if self.options.wordsearch != None:
                calendarEventDataList = self.getTextQueryEvents(self.options.wordsearch)
            elif self.options.startdate != None:
                if self.options.enddate != None:
                    calendarEventDataList = self.getDateRangedEvents(self.options.startdate,self.options.enddate)
                else:
                    print >> sys.stdout, "--startdate provided with no --enddate."
                    self.parser.print_help()
            elif self.options.allevents == True:
                calendarEventDataList = self.getAllEvents()
            else:
                calendarEventDataList = self.getFutureEvents(self.options.daysahead)

            ################ PREPARE FOR OUTPUT ##############################

            self.logInfo("Processing output...")

            if self.options.template == None:
                # get the indent spacing sorted out
                if self.options.indent > 0:
                    indent = self.getSpaces(self.options.indent)
                else:
                    indent = ""

                # create default template
                template = indent+"[title]\n" + indent + "From [starttime] [duration]\n" + indent + "At [location]\n" + indent + "\"[description]\"\n" + indent + "With [who]\n"
            else:
                # load the template file contents
                try:
                    fileinput = codecs.open(os.path.expanduser(self.options.template), encoding='utf-8')
                    template = fileinput.read()
                    fileinput.close()
                    # lose the final "\n" which should always be there...
                    template = template[0:len(template)-1]
                except:
                    self.logError("Template file no found!")
                    sys.exit(2)

            ################ PROCESS OUTPUT #########################################
            calendarEventCount = 0
            calendarEventDataList.sort()

            if len(calendarEventDataList) > 0:
                # walk through the calendar events
                for calendarEventData in calendarEventDataList:

                    # keep a tally of events output, if past the limit then exit
                    if self.options.limit <> 0:
                        calendarEventCount = calendarEventCount+1
                        if calendarEventCount > self.options.limit:
                            sys.exit()

                    # collect calendar event data and format as we go
                    title = calendarEventData.title
                    starttime = self.getDatetimeFromWhen(calendarEventData.starttime)
                    endtime = self.getDatetimeFromWhen(calendarEventData.endtime)

                    location = calendarEventData.location
                    if location <> None:
                        #location = self.getWrappedText(location, self.options.maxwidth, indent)
                        if len(location) > self.options.maxwidth:
                            location = location[0:self.options.maxwidth].replace("\n","")+"..."

                    description = calendarEventData.description
                    if description <> None:
                        #description = self.getWrappedText(description, self.options.maxwidth, indent)
                        if len(description) > self.options.maxwidth:
                            description = description[0:self.options.maxwidth].replace("\n","")+"..."

                    who = calendarEventData.who
                    if who != None:
                        if self.options.nowho == True:
                            who = None
                        else:
                            who = ";".join(who)+";"
                            who = re.sub("@.*?;",", ",who).rstrip(", ")
                            if len(who) > self.options.maxwidth:
                                who = who[0:self.options.maxwidth]+"..."
                                #who = ";".join(who).replace(";",", ")
                                #who = self.getWrappedText(who, self.options.maxwidth, indent)

                    # output event data using the template
                    output = self.getOutputFromTemplate(template, title, starttime, endtime, location, description, who)

                    output = self.getMadeSafeOutput(output)
                    print output #.encode("utf-8")

            else:
                self.logInfo("No Events to display...")

        except Exception,e:
            self.logError("writeOutput:Unexpected error:" + traceback.format_exc())
            
def main():
    """Runs the conkyGoogleCalendar application with the provided username and
    and password values.  Authentication credentials are required."""

    ################ COMMAND LINE ARGUMENTS #################################
    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.version == True:

        print >> sys.stdout,"conkyGoogleCalendar v.2.16"

    else:

        if options.username == None:
            print >> sys.stdout, "A username was not given!"
            sys.exit(2)

        if options.verbose == True:
            print >> sys.stdout, "*** INITIAL OPTIONS:"
            print >> sys.stdout, "    username:",options.username
            print >> sys.stdout, "    password:",options.password
            print >> sys.stdout, "    daysahead:",options.daysahead
            print >> sys.stdout, "    startdate:",options.startdate
            print >> sys.stdout, "    enddate:",options.enddate
            print >> sys.stdout, "    allevents:",options.allevents
            print >> sys.stdout, "    wordsearch:",options.wordsearch
            print >> sys.stdout, "    limit:",options.limit
            print >> sys.stdout, "    template:",options.template
            print >> sys.stdout, "    dateformat:",options.dateformat
            print >> sys.stdout, "    indent:",options.indent
            print >> sys.stdout, "    nowho:",options.nowho
            print >> sys.stdout, "    verbose:",options.verbose
            print >> sys.stdout, "    errorlogfile:",options.errorlogfile
            print >> sys.stdout, "    infologfile:",options.infologfile

        googlecalendarinfo = GoogleCalendarInfo(options)
        googlecalendarinfo.writeOutput()

if __name__ == '__main__':
    main()
    sys.exit()
