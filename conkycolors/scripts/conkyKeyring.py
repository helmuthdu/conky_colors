#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyKeyring.py is a simple python script to store/edit/delete passwords
# for use in the conky scripts that utilise stored passwords
#
#  Author: Kaivalagi
# Created: 26/02/2011
from keyring import get_password, set_password
from datetime import datetime
from optparse import OptionParser
import sys
import codecs
import os

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-u", "--username", dest="username", type="string", metavar="USERNAME", help=u"The username where the password will be stored against, this is usually an email address or other account identifier which is used for login purposes")
        self.parser.add_option("-p", "--password", dest="password", type="string", metavar="PASSWORD", help=u"The password to be stored safely, leave unset to retrieve the password")
        self.parser.add_option("-d", "--delete", dest="delete", default=False, action="store_true", help=u"If set the password associated with the username given is deleted")
        self.parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help=u"Request verbose output, not a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")                

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class Keyring:
    
    options = None
    
    def __init__(self,options):
        
        self.options = options
        
    def ApplyKeyringOperations(self):
        
        try:
            
            if self.options.username == None:
                self.logError("A username must be set for any keyring operations to be made")
                return
            
            if self.options.delete == True:
                self.logInfo("Clearing password for "+self.options.username)
                set_password("conky", self.options.username, "")
            else:
                if self.options.password != None:
                    self.logInfo("Storing password for "+self.options.username)
                    set_password("conky", self.options.username, self.options.password)
                else:
                    self.logInfo("Retrieving password for "+self.options.username)
                    password = get_password("conky", self.options.username)
                    if password != None:
                        print password
                    else:
                        self.logInfo("Password not found!")
        
        except Exception, e:
            self.logError("ApplyKeyringOperations error:" + e.__str__())   
        
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
            
if __name__ == "__main__":
    
    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.version == True:
        print >> sys.stdout,"conkyKeyring v.1.01"
    else:
        if options.verbose == True:
            print >> sys.stdout, "*** INITIAL OPTIONS:"
            print >> sys.stdout, "    username:", options.username
            print >> sys.stdout, "    password:", options.password
            print >> sys.stdout, "    delete:", options.delete
            print >> sys.stdout, "    verbose:", options.verbose
            print >> sys.stdout, "    errorlogfile:",options.errorlogfile
            print >> sys.stdout, "    infologfile:",options.infologfile            

    keyring = Keyring(options)
    keyring.ApplyKeyringOperations()
    
