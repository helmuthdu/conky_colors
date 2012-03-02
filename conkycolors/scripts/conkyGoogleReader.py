#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyEmail.py is a simple python script to gather 
# details of google reader subscriptions for use in conky.
#
#  Author: Kaivalagi
# Created: 09/07/2008
#
#    18/05/2009    Updated to expand ~ based template paths
#    14/12/2009    Updated to work with new authentication requirements, old method stopped working for some reason
from datetime import datetime
from optparse import OptionParser
from xml.dom import minidom
from keyring import get_password
import codecs
import socket
import sys
import traceback
import urllib
import urllib2
import os

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-u","--username",dest="username", type="string", metavar="USERNAME", help=u"username to login with")
        self.parser.add_option("-p","--password",dest="password", type="string", metavar="PASSWORD", help=u"Password to login with, if not set the username is used to fetch a 'conky' password from the keyring")
        self.parser.add_option("-t","--template",dest="template", type="string", metavar="FILE", help=u"Template file determining the format for each rss feed summary. Use the following placeholders: [unreadcount], [name], [url]")
        self.parser.add_option("-s","--summarytemplate",dest="summarytemplate", type="string", metavar="FILE", help=u"Template file determining the format for summary output. Use the following placeholders: [totalfeedscount], [unreadfeedscount], [unreadfeeditemscount]")
        self.parser.add_option("-S","--summaryoutput",dest="summaryoutput", default=False, action="store_true", help=u"Request summary output rather than each feeds details")
        self.parser.add_option("-c","--connectiontimeout",dest="connectiontimeout", type="int", default=10, metavar="NUMBER", help=u"[default: %default] Define the number of seconds before a connection timeout can occur.")
        self.parser.add_option("-v","--verbose",dest="verbose", default=False, action="store_true", help=u"Request verbose output, no a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")                

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class FeedData:
    def __init__(self, name, url, unreadcount):
        self.name = name
        self.url = url
        self.unreadcount = unreadcount

    def __cmp__(self, other):
        return cmp(int(other.unreadcount),int(self.unreadcount))
    
    def __str__(self):
        return str(self.name + " - " + self.unreadcount)
        
class GoogleReader:

    def __init__(self,options):

        try:
            
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
                                
            self.logInfo("Initialising google reader...")
            
            socket.setdefaulttimeout(self.options.connectiontimeout)

        except Exception,e:
            self.logError("GoogleReader Initialisation:Unexpected error:" + e.__str__()+traceback.format_exc())
            
    def writeOutput(self):
        
        auth_header = self.getAuthorizationHeader()
        
        if auth_header != None:
            
            self.logInfo("Processing output...")
            
            if self.options.template == None:               
                # create default template
                template = "[unreadcount] [name] - [url]\n"
            else:
                # load the template file contents
                try:
                    #fileinput = open(self.options.template)
                    fileinput = codecs.open(os.path.expanduser(self.options.template), encoding='utf-8')
                    template = fileinput.read()
                    fileinput.close()
                    # lose the final "\n" which should always be there...
                    template = template[0:len(template)-1]
                except:
                    self.logError("Template file no found!")
                    sys.exit(2)

            if self.options.summarytemplate == None:               
                # create default template
                summarytemplate = "[unreadfeeditemscount] unread feed items, [unreadfeedscount]/[totalfeedscount] feeds have unread content.\n"
            else:
                # load the template file contents
                try:
                    #fileinput = open(self.options.template)
                    fileinput = codecs.open(os.path.expanduser(self.options.summarytemplate), encoding='utf-8')
                    summarytemplate = fileinput.read()
                    fileinput.close()
                    # lose the final "\n" which should always be there...
                    summarytemplate = summarytemplate[0:len(summarytemplate)-1]
                except:
                    self.logError("Template file no found!")
                    sys.exit(2)
                                                    
            totalfeedscount, unreadfeedscount, unreadfeeditemscount, feeds = self.getUnreadItems(auth_header)

            output = ""
            if self.options.summaryoutput == True:
                output = self.getOutputFromSummaryTemplate(summarytemplate, totalfeedscount, unreadfeedscount, unreadfeeditemscount)
            else:
                for feeddata in feeds:
                    output = output + self.getOutputFromTemplate(template, feeddata.unreadcount, feeddata.name, feeddata.url)

            print output.encode("utf-8")

    def getOutputFromTemplate(self, template, unreadcount, name, url):
        
        try:
            
            output = template
    
            output = output.replace("[unreadcount]",unreadcount)
            output = output.replace("[name]",name)
            output = output.replace("[url]",url)

            return output
        
        except Exception,e:
            self.logError("getOutputFromTemplate:Unexpected error:" + e.__str__())
            return ""

    def getOutputFromSummaryTemplate(self, summarytemplate, totalfeedscount, unreadfeedscount, unreadfeeditemscount):
        
        try:
            
            output = summarytemplate
    
            output = output.replace("[totalfeedscount]",totalfeedscount)
            output = output.replace("[unreadfeedscount]",unreadfeedscount)
            output = output.replace("[unreadfeeditemscount]",unreadfeeditemscount)
            

            return output
        
        except Exception,e:
            self.logError("getOutputFromSummaryTemplate:Unexpected error:" + e.__str__())
            return ""
        
    def getAuthorizationHeader(self):
        
        # Authenticate to obtain SID
        auth_url = 'https://www.google.com/accounts/ClientLogin'
        auth_req_data = urllib.urlencode({'Email': self.options.username,
                                          'Passwd': self.options.password,
                                          'service': 'reader'})
        auth_req = urllib2.Request(auth_url, data=auth_req_data)
        auth_resp = urllib2.urlopen(auth_req)
        auth_resp_content = auth_resp.read()
        auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
        AUTH = auth_resp_dict["Auth"]
        
        # Create a header using the AUTH key 
        header = {"Authorization" : "GoogleLogin auth=%s"%AUTH}
        
        return header
        
    def getUnreadItems(self, auth_header):
                
        url = "https://www.google.com/reader/api/0/unread-count?all=true"
        request = urllib2.Request(url, None, auth_header)
        response = urllib2.urlopen(request)
        unreadxml = response.read()

        url = "https://www.google.com/reader/api/0/subscription/list"
        request = urllib2.Request(url, None, auth_header)
        response = urllib2.urlopen(request)
        namesxml = response.read()
                    
        if '<object>' in unreadxml:
            feedlist = minidom.parseString(unreadxml).getElementsByTagName('string')
            namelist = minidom.parseString(namesxml).getElementsByTagName('string')

            feeds = []
            unreadcount = 0
            unreadfeedcount = 0
            unreadfeeditemscount = 0
            
            for nodeFeed in feedlist:
                
                feedurl = nodeFeed.firstChild.toxml()          
                    
                # ignore user/ based nodes, only concerned with feed/ based nodes
                if feedurl.startswith("feed/") == True:
                    
                    unreadcount = nodeFeed.nextSibling.firstChild.toxml()
                    
                    for nodeName in namelist:
                        nodeText = nodeName.firstChild.toxml()
                        if nodeText.startswith("feed/"):
                            if nodeText == feedurl:
                                feedname = nodeName.nextSibling.firstChild.toxml()
                                break
                                
                    feedurl = feedurl.lstrip("feed/")
                    
                    #feeds.append((unreadcount , feedurl, feedname))
                    feedData = FeedData(feedname, feedurl, unreadcount)
                    feeds.append(feedData)
                    
                    unreadfeeditemscount = unreadfeeditemscount + int(unreadcount)
                    unreadfeedcount = unreadfeedcount + 1
                else:
                    pass #invalid feedurl?
            
            totalfeedcount = len(namelist)
            
            feeds.sort()
            return str(totalfeedcount), str(unreadfeedcount), str(unreadfeeditemscount), feeds
        else:
            return 0        

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
                        
def main():

    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.version == True:
        
        print >> sys.stdout,"conkyGoogleReader v.1.08"
        
    else:
        
        if options.username == None:
            print >> sys.stdout, "A username was not given!"
            sys.exit(2)
                    
        if options.verbose == True:
            print >> sys.stdout, "username:",options.username
            print >> sys.stdout, "password:",options.password
            print >> sys.stdout, "template:",options.template
            print >> sys.stdout, "summarytemplate:",options.summarytemplate
            print >> sys.stdout, "summaryoutput:",options.summaryoutput
            print >> sys.stdout, "verbose:",options.verbose
    
        # create new google reader object
        greader = GoogleReader(options)
        greader.writeOutput()

if __name__ == '__main__':
    main()
    sys.exit()
