#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyText.py is a simple python script to format a delimited text file with
# an accompanying template, for use in conky.
#
#  Author: Kaivalagi
# Created: 28/10/2008
from datetime import datetime
from optparse import OptionParser
import sys
import codecs
import os

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-t", "--template", dest="template", type="string", metavar="FILE", help=u"location of the template file to define the layout of output")
        self.parser.add_option("-f", "--textfile", dest="textfile", type="string", metavar="FILE", help=u"location of the text file to output.")
        self.parser.add_option("-d", "--delimiter", dest="delimiter", default=";", type="string", metavar="FILE", help=u"default:[%default]Specify the delimiter to use when splitting out a line of text into formatted segments")
        self.parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help=u"Request verbose output, not a good idea when running through conky!")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")                

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class TextFormatter:
    
    options = None
    
    def __init__(self,options):
        
        self.options = options
        
    def writeOutput(self):
        
        try:
        
            self.logInfo("Loading templates and text file...")
            
            output = u""
            textfilepath = self.options.textfile
            templatefilepath = self.options.template
            delimiter = self.options.delimiter 
            
            # load the textfile lines...
            fileinput = codecs.open(os.path.expanduser(textfilepath), encoding='utf-8')
            textfilelines = fileinput.read().split("\n")
            fileinput.close() 
    
            # load the template segments
            fileinput = codecs.open(os.path.expanduser(templatefilepath), encoding='utf-8')
            templatesegments = fileinput.read().rstrip("\n").split(";")
            fileinput.close() 
    
            self.logInfo("Building output for each line of text...")
            
            # handle the each text line, dealing with each segment and applying the template for that segment
                    
            # get each line and split it into it's segments
            for line in textfilelines:
                
                if len(line) > 0:
                    
                    linesegments = line.split(delimiter)
                    
                    # for each segment add the template formatting
                    for segmentindex in range(0, len(linesegments)):
                        linesegments[segmentindex] = templatesegments[segmentindex]+linesegments[segmentindex]
        
                    # re-join the line segments for this line
                    output = output + "".join(linesegments) + "\n"
                    
            output = output.rstrip("\n")
            
            print output.encode("utf-8")
        
        except Exception, e:
            self.logError("writeOutput error:" + e.__str__())   
        
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

    if options.verbose == True:
        print >> sys.stdout, "*** INITIAL OPTIONS:"
        print >> sys.stdout, "    template:", options.template
        print >> sys.stdout, "    textfile:", options.textfile
        print >> sys.stdout, "    delimiter:", options.delimiter
        print >> sys.stdout, "    verbose:", options.verbose
        print >> sys.stdout, "    errorlogfile:",options.errorlogfile
        print >> sys.stdout, "    infologfile:",options.infologfile            

    textFormatter = TextFormatter(options)
    textFormatter.writeOutput()
    
