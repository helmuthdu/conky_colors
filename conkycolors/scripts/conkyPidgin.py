#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyPidgin.py is a simple python script to display
# details of pidgin buddies, for use in conky.
#
#  Author: Kaivalagi
# Created: 03/11/2008

from datetime import datetime
from htmlentitydefs import name2codepoint
from optparse import OptionParser
import re
import sys
import traceback
import codecs
import os
import stat
try:
    import dbus
    DBUS_AVAIL = True
except ImportError:
    # Dummy D-Bus library
    class _Connection:
        get_object = lambda *a: object()
    class _Interface:
        __init__ = lambda *a: None
        ListNames = lambda *a: []
    class Dummy: pass
    dbus = Dummy()
    dbus.Interface = _Interface
    dbus.service = Dummy()
    dbus.service.method = lambda *a: lambda f: f
    dbus.service.Object = object
    dbus.SessionBus = _Connection
    DBUS_AVAIL = False


class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-t", "--template", dest="template", type="string", metavar="FILE", help=u"Template file determining the format for each buddy's data or account info. Use the following placeholders for default buddy output: [name], [alias], [group], [status], [status_message]. If outputting an account listing use these placeholders: [name], [protocol], [status]")
        self.parser.add_option("-L", "--accountlisting", dest="accountlisting", default=False, action="store_true", help=u"Show account listing with status rather than buddies")
        self.parser.add_option("-o", "--onlineonly", dest="onlineonly", default=False, action="store_true", help=u"Only show online buddies. If outputting account listings this option limits it to enabled only.")
        self.parser.add_option("-a", "--availableonly", dest="availableonly", default=False, action="store_true", help=u"Only show available buddies. If outputting account listings this option limits it to enabled only.")
        self.parser.add_option("-f", "--offlineonly", dest="offlineonly", default=False, action="store_true", help=u"Only show offline buddies. If outputting account listings this option limits it to disabled only.")
        self.parser.add_option("-i", "--ignorelist", dest="ignorelist", type="string", metavar="LIST", help=u"A comma delimited list of groups to ignore. Partial text matches on group will be ignored if found")
        self.parser.add_option("-I", "--includelist", dest="includelist", type="string", metavar="LIST", help=u"A comma delimited list of groups to include. Partial text matches on group will be included if found. The ignorelist, if used, takes precedence. if this list is omitted all groups will be included unless ignored.")
        self.parser.add_option("-C", "--chattingtext", dest="chattingtext", type="string", default="Chatting", metavar="TEXT", help=u"[default: %default] Text to use for chatting status output")
        self.parser.add_option("-A", "--availabletext", dest="availabletext", type="string", default="Available", metavar="TEXT", help=u"[default: %default] Text to use for available status output")
        self.parser.add_option("-U", "--unavailabletext", dest="unavailabletext", type="string", default="Unavailable", metavar="TEXT", help=u"[default: %default] Text to use for unavailable status output")
        self.parser.add_option("-N", "--invisibletext", dest="invisibletext", type="string", default="Invisible", metavar="TEXT", help=u"[default: %default] Text to use for invisible status output")
        self.parser.add_option("-W", "--awaytext", dest="awaytext", type="string", default="Away", metavar="TEXT", help=u"[default: %default] Text to use for away status output")
        self.parser.add_option("-M", "--mobiletext", dest="mobiletext", type="string", default="Mobile", metavar="TEXT", help=u"[default: %default] Text to use for mobile status output")
        self.parser.add_option("-F", "--offlinetext", dest="offlinetext", type="string", default="Offline", metavar="TEXT", help=u"[default: %default] Text to use for offline status output")
        self.parser.add_option("-l", "--limit", dest="limit", type="int", default=0, metavar="NUMBER", help=u"[default: %default] Set a limit to the number of buddies displayed, by default no limitation is made")
        self.parser.add_option("-s", "--sortby", dest="sortby", type="string", default="DEFAULT", metavar="METHOD", help=u"[default: %default] Sort options for both buddy and account listings. These are DEFAULT, NAME, ALIAS, GROUP, STATUS or LOGACTIVITY. ALIAS, GROUP and LOGACTIVITY sort options are not applicable for account listings so appropriate sorting methods are used instead. LOGACTIVITY is useful when limiting the list size with the limit option. ")
        self.parser.add_option("-d", "--distinctaliases", dest="distinctaliases", default=False, action="store_true", help=u"Request any duplicate aliases to be removed from the output, these could be for the same person in different IM networks.")
        self.parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help=u"Request verbose output, not a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class PidginData:

    def __init__(self, name, alias, group, status, status_message, activitydatetime):
        self.name = name
        self.alias = alias
        self.group = group
        self.status = status
        self.status_message = status_message
        self.activitydatetime = activitydatetime

    def __cmp__(self, other):
        return cmp(str(self.status)+self.group.lower()+self.alias.lower(), str(other.status)+other.group.lower()+other.alias.lower())

    def __str__(self):
        return str(self.name+"("+self.alias+")")

class PidginAccountData:

    def __init__(self, name, protocol, status):
        self.name = name
        self.protocol = protocol
        self.status = status

    def __cmp__(self, other):
        return cmp(str(self.status)+self.protocol.lower()+self.name.lower(), str(other.status)+other.protocol.lower()+other.name.lower())

    def __str__(self):
        return str(self.name+"("+self.protocol+") - "+self.status)
    
class PidginInfo:

    STATUS_OFFLINE = 1
    STATUS_AVAILABLE = 2
    STATUS_UNAVAILABLE = 3
    STATUS_INVISIBLE = 4
    STATUS_AWAY = 5
    STATUS_EXTENDED_AWAY = 6
    STATUS_MOBILE = 7
    STATUS_TUNE = 8

    TEXT_CHATTING = 1
    TEXT_AVAILABLE = 2
    TEXT_UNAVAILABLE = 3
    TEXT_INVISIBLE = 4
    TEXT_AWAY = 5
    TEXT_MOBILE = 6
    TEXT_OFFLINE = 7

    PIDGIN_LOGS_PATH = "~/.purple/logs"

    def __init__(self, options):
        self.options = options

    def testDBus(self, bus, interface):
        obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        dbus_iface = dbus.Interface(obj, 'org.freedesktop.DBus')
        avail = dbus_iface.ListNames()
        return interface in avail

    def getBuddyStatusText(self, status):

        if status == self.TEXT_CHATTING:
            return self.options.chattingtext
        elif status == self.TEXT_AVAILABLE:
            return self.options.availabletext
        elif status == self.TEXT_UNAVAILABLE:
            return self.options.unavailabletext
        elif status == self.TEXT_INVISIBLE:
            return self.options.invisibletext
        elif status == self.TEXT_AWAY:
            return self.options.awaytext
        elif status == self.TEXT_MOBILE:
            return self.options.mobiletext
        elif status == self.TEXT_OFFLINE:
            return self.options.offlinetext
        else:
            return ""

    def getAccountStatusText(self, enabled):
        
        if enabled == True:
            return "Enabled"
        else:
            return "Disabled"
        
    def getOutputFromTemplate(self, template, name, alias, group, status, status_message):

        try:

            output = template

            output = output.replace("[name]",name)
            output = output.replace("[alias]",alias)
            output = output.replace("[group]",group)
            output = output.replace("[status]",self.getBuddyStatusText(status))
            output = output.replace("[status_message]",status_message)

            # get rid of any excess crlf's
            output = output.rstrip(" \n")

            return output

        except Exception,e:
            self.logError("getOutputFromTemplate:Unexpected error:" + e.__str__())
            return ""


    def getOutputFromAccountListingTemplate(self, template, name, protocol, enabled):

        try:

            output = template

            output = output.replace("[name]",name)
            output = output.replace("[protocol]",protocol)
            output = output.replace("[status]",self.getAccountStatusText(enabled))

            # get rid of any excess crlf's
            output = output.rstrip(" \n")

            return output

        except Exception,e:
            self.logError("getOutputFromAccountListingTemplate:Unexpected error:" + e.__str__())
            return ""

    def getPidginData(self):

        pidginDataList = []
        pidginAccountDataList = []

        try:

            bus = dbus.SessionBus()

            if self.testDBus(bus, 'im.pidgin.purple.PurpleService'):

                    self.logInfo("Setting up dbus interface")

                    remote_object = bus.get_object("im.pidgin.purple.PurpleService","/im/pidgin/purple/PurpleObject")
                    iface = dbus.Interface(remote_object, "im.pidgin.purple.PurpleService")

                    self.logInfo("Calling dbus interface for IM data")

                    # get all accounts (incl disabled ones)
                    acctList = iface.PurpleAccountsGetAll()
                    acctActiveList = iface.PurpleAccountsGetAllActive()
                
                    # Iterate through every active account
                    for acctID in acctList:

                        acctUsername = iface.PurpleAccountGetUsername(acctID)
                        acctProtocol = iface.PurpleAccountGetProtocolName(acctID)

                        acctEnabled = False
                        for acctActiveID in acctActiveList:
                            if acctID == acctActiveID:
                                acctEnabled = True

                        if self.options.accountlisting == True:
                            
                            # should we gather accounts for output
                            addAccount = True
                            if (self.options.availableonly == True or self.options.onlineonly == True):
                                addAccount = acctEnabled
                            elif (self.options.offlineonly == True):
                                addAccount = not acctEnabled
                            else:
                                addAccount = True
                                
                            if addAccount == True:
                                self.logInfo("Adding account data for name '%s', status '%s'"%(acctUsername, acctEnabled))
                                
                                pidginAccountData = PidginAccountData(acctUsername, acctProtocol, acctEnabled)
                                pidginAccountDataList.append(pidginAccountData)

                        elif acctEnabled == True:
                            
                            # get all the buddies associated with that account
                            buddies = iface.PurpleFindBuddies(acctID,"")
    
                            for buddyid in buddies:
    
                                groupid = iface.PurpleBuddyGetGroup(buddyid)
    
                                # get initial data
                                alias = iface.PurpleBuddyGetAlias(buddyid)
                                name = iface.PurpleBuddyGetName(buddyid)
                                online = iface.PurpleBuddyIsOnline(buddyid)
                                group = iface.PurpleGroupGetName(groupid)
    
                                if self.ignoreGroup(group) == False:
    
                                    if self.includeGroup(group) == True:
    
                                        addBuddy = False
    
                                        if self.options.onlineonly == True:
                                            if online == 1:
                                                addBuddy = True
                                        elif self.options.offlineonly == True:
                                            if online == 0:
                                                addBuddy = True
                                        else:
                                            addBuddy = True
    
                                        if addBuddy == True:
    
                                        # determine whether to show this buddies details based on onlineonly option
                                        #if online == 1 or self.options.onlineonly == False:
    
                                            available = 0
    
                                            # retrieve buddy status
                                            presenceid = iface.PurpleBuddyGetPresence(buddyid)
                                            status = iface.PurplePresenceGetActiveStatus(presenceid)
    
                                            # get extended message if set
                                            status_message = self.getCleanText(iface.PurpleStatusGetAttrString(status, "message")) # getCleanText needed for google encoded text
    
                                            # get the status type, id and text
                                            statustype = iface.PurpleStatusGetType(status)
                                            statusid = iface.PurpleStatusTypeGetPrimitive(statustype)
                                            statustypetext = iface.PurpleStatusTypeGetId(statustype)
    
                                            if online == 1:
                                                if self.isBuddyChatting(name,iface):
                                                    statustext = self.TEXT_CHATTING
                                                    available = 1
                                                else:
                                                    if statusid == self.STATUS_AVAILABLE:
                                                        statustext = self.TEXT_AVAILABLE
                                                        available = 1
    
                                                    elif statusid == self.STATUS_UNAVAILABLE:
                                                        statustext = self.TEXT_UNAVAILABLE
    
                                                    elif statusid == self.STATUS_INVISIBLE:
                                                        statustext = self.TEXT_INVISIBLE
    
                                                    elif statusid == self.STATUS_AWAY or statusid == self.STATUS_EXTENDED_AWAY:
                                                        statustext = self.TEXT_AWAY
    
                                                    elif statusid == self.STATUS_MOBILE:
                                                        statustext = self.TEXT_MOBILE
    
                                                    elif statusid == self.STATUS_TUNE:
                                                        #TODO: need icon for STATUS_TUNE whatever that is...
                                                        statustext = self.TEXT_AVAILABLE
    
                                                    else: # catch all in case no match on statustype, guess available
                                                        statustext = self.TEXT_AVAILABLE
                                            else:
                                                statustext = self.TEXT_OFFLINE
    
                                            # determine whether to show this buddies details based on availableonly option
                                            if available == 1 or self.options.availableonly == False:
    
                                                # get latest activity datetime
                                                activitydatetime = self.getBuddyActivityDatetime(self.PIDGIN_LOGS_PATH, name)
    
                                                # see if we should ignore this buddy based on duplicate aliases
                                                ignore = False
                                                if self.options.distinctaliases == True:
                                                    for pidginData in pidginDataList:
                                                        if pidginData.alias == alias:
                                                            ignore = True
                                                            break
                                                
                                                if ignore == True:
                                                    
                                                    self.logInfo("Skipping IM data for buddy '%s' as this alias is already in the output list"%(alias))
                                                    
                                                else:
                                                    
                                                    self.logInfo("Adding IM data for buddy '%s', status type '%s'"%(alias, statustypetext))
                                                    
                                                    pidginData = PidginData(name, alias, group, statustext, status_message, activitydatetime)
                                                    pidginDataList.append(pidginData)


                    # tidy up
                    del iface
                    del remote_object
                    del bus

            # sort the list by option
            if self.options.sortby == "DEFAULT":
                pidginAccountDataList.sort(key=lambda obj: (str(obj.status)+obj.protocol.lower()+obj.name.lower()))
                pidginDataList.sort(key=lambda obj: (str(obj.status)+obj.group.lower()+alias.lower()))
            elif self.options.sortby == "NAME":
                pidginAccountDataList.sort(key=lambda obj: (obj.name.lower()+str(obj.status)+obj.protocol.lower()))
                pidginDataList.sort(key=lambda obj: (obj.name+obj.alias+obj.group+str(obj.status)))
            elif self.options.sortby == "ALIAS":
                pidginAccountDataList.sort(key=lambda obj: (obj.name.lower()+str(obj.status)+obj.protocol.lower()))
                pidginDataList.sort(key=lambda obj: (obj.alias+obj.name+obj.group+str(obj.status)))
            elif self.options.sortby == "GROUP":
                pidginAccountDataList.sort(key=lambda obj: (obj.name.lower()+str(obj.status)+obj.protocol.lower()))
                pidginDataList.sort(key=lambda obj: (obj.group+obj.name+obj.alias+str(obj.status)))
            elif self.options.sortby == "STATUS":
                pidginAccountDataList.sort(key=lambda obj: (obj.name.lower()+str(obj.status)+obj.protocol.lower()))
                pidginDataList.sort(key=lambda obj: str(obj.status)+obj.name+obj.alias+obj.group)
            elif self.options.sortby == "LOGACTIVITY":
                pidginAccountDataList.sort(key=lambda obj: (str(obj.status)+obj.protocol.lower()+obj.name.lower()))
                pidginDataList.sort(key=lambda obj: obj.activitydatetime,reverse=True)
            else:
                raise Exception("Invalid sortby option provided")
            
            return pidginAccountDataList, pidginDataList

        except Exception, e:
            self.logError("Unknown error when calling getPidginData:" + e.__str__())

    def writeOutput(self):

        if self.options.template == None:

            if self.options.accountlisting == True:
                # create default account summary template
                template = "[name] ([protocol]) - [status]"
            else:
                # create default template
                template = "${color0}${font Webdings:size=14})${font}${color}   [alias] $alignr${color2}[group]${color}"
        else:
            # load the template file contents
            try:
                fileinput = codecs.open(os.path.expanduser(self.options.template), encoding='utf-8')
                template = fileinput.read()
                fileinput.close()
            except:
                self.logError("Template file no found!")
                sys.exit(2)

        try:

            pidginAccountDataList, pidginDataList = self.getPidginData()

            self.logInfo("Outputting buddy information...")

            buddyCount = 0
            output = ""
                
            for pidginAccountData in pidginAccountDataList:

                # keep a tally of buddies output, if past the limit then exit
                if self.options.limit <> 0:
                    buddyCount = buddyCount+1
                    if buddyCount > self.options.limit:
                        break

                # output pidgin buddy data using the template
                output += self.getOutputFromAccountListingTemplate(template, pidginAccountData.name, pidginAccountData.protocol, pidginAccountData.status)+"\n"
                
            for pidginData in pidginDataList:

                # keep a tally of buddies output, if past the limit then exit
                if self.options.limit <> 0:
                    buddyCount = buddyCount+1
                    if buddyCount > self.options.limit:
                        break

                # output pidgin buddy data using the template
                output += self.getOutputFromTemplate(template, pidginData.name, pidginData.alias, pidginData.group, pidginData.status, pidginData.status_message)+"\n"
                    
            output = self.getMadeSafeOutput(output)
            output = output.rstrip(" \n")
            print output.encode("utf-8")

        except SystemExit:
            self.logError("System Exit!")
            return u""
        except Exception, e:
            traceback.print_exc()
            self.logError("Unknown error when calling writeOutput:" + e.__str__())
            return u""

    def getBuddyActivityDatetime(self, basefolder, buddyname):

        basefolder = os.path.expanduser(basefolder)
        latestmodifieddatetime = datetime(2000, 1, 1, 0, 0)

        # if the folder passed in is non existant return an empty list
        if os.path.exists(basefolder):

            # for each file or folder
            for root, dirs, files in os.walk(basefolder):

                for dir in dirs:
                    if dir == buddyname:

                        buddypath = os.path.join(root,dir)
                        moddatetime = self.getLatestLogFileModificationDatetime(buddypath, latestmodifieddatetime)
                        if moddatetime > latestmodifieddatetime:
                            latestmodifieddatetime = moddatetime

        return latestmodifieddatetime

    def getLatestLogFileModificationDatetime(self, folderpath, latestmodifieddatetime):

        for file in os.listdir(folderpath):
            filepath = os.path.join(folderpath,file)
            if os.path.isfile(filepath):
                modifieddate = datetime.fromtimestamp(os.stat(filepath)[stat.ST_MTIME])
                if modifieddate > latestmodifieddatetime:
                    latestmodifieddatetime = modifieddate

        return latestmodifieddatetime

    def isBuddyChatting(self,name,iface):
        imids = iface.PurpleGetIms()
        for imid in imids:
            convname = iface.PurpleConversationGetName(imid)
            if convname == name:
                return True

        return False

    def ignoreBuddy(self, name, alias):

        if self.options.ignorelist != None:

            # for each text in the ignore list, should we be ignoring the buddy
            for ignore in self.options.ignorelist.split(","):
                # has the buddy been found in the list item
                if name.lower().find(ignore.lower()) != -1 or alias.lower().find(ignore.lower()) != -1:
                    return True

            return False

        else:
            return False

    def includeBuddy(self, name, alias):

        if self.options.includelist != None:

            # for each text in the ignore list, should we be ignoring the buddy
            for include in self.options.includelist.split(","):
                # has the buddy been found in the list item
                if name.lower().find(include.lower()) != -1 or alias.lower().find(include.lower()) != -1:
                    return True

            return False

        else:
            return True

    def ignoreGroup(self, group):

        if self.options.ignorelist != None:

            # for each text in the ignore list, should we be ignoring the buddy in the group
            for ignore in self.options.ignorelist.split(","):
                # has the group been found in the list item
                if group.lower().find(ignore.lower()) != -1:
                    return True

            return False

        else:
            return False

    def includeGroup(self, group):

        if self.options.includelist != None:

            # for each text in the ignore list, should we be ignoring the buddy in the group
            for include in self.options.includelist.split(","):
                # has the group been found in the list item
                if group.lower().find(include.lower()) != -1:
                    return True

            return False

        else:
            return True

    def getCleanText(self,text):
        text = text.replace("&apos;","'") # workaround for shitty xml codes not compliant with html
        text = re.sub('<(.|\n)+?>','',text) # remove any html tags
        return re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: chr(name2codepoint[m.group(1)]), text)

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

def main():

    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.version == True:
        print >> sys.stdout,"conkyPidgin v.2.17"
    else:
        if options.verbose == True:
            print >> sys.stdout, "*** INITIAL OPTIONS:"
            print >> sys.stdout, "    template:", options.template
            print >> sys.stdout, "    onlineonly:", options.onlineonly
            print >> sys.stdout, "    availableonly:", options.availableonly
            print >> sys.stdout, "    ignorelist:", options.ignorelist
            print >> sys.stdout, "    includelist:", options.includelist
            print >> sys.stdout, "    chattingtext:", options.chattingtext
            print >> sys.stdout, "    availabletext:", options.availabletext
            print >> sys.stdout, "    unavailabletext:", options.unavailabletext
            print >> sys.stdout, "    invisibletext:", options.invisibletext
            print >> sys.stdout, "    awaytext:", options.awaytext
            print >> sys.stdout, "    mobiletext:", options.mobiletext
            print >> sys.stdout, "    offlinetext:", options.offlinetext
            print >> sys.stdout, "    sortby:", options.sortby            
            print >> sys.stdout, "    verbose:", options.verbose
            print >> sys.stdout, "    errorlogfile:",options.errorlogfile
            print >> sys.stdout, "    infologfile:",options.infologfile

        buddyinfo = PidginInfo(options)
        buddyinfo.writeOutput()

if __name__ == '__main__':
    main()
    sys.exit()
