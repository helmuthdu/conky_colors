#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyExaile.py is a simple python script to gather 
# details of from exaile for use in conky.
#
#  Author: Kaivalagi
# Created: 21/09/2008

from PIL import Image
from StringIO import StringIO
from datetime import datetime
from optparse import OptionParser
import codecs
import os
import sys
import traceback

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
        self.parser.add_option("-t", "--template", dest="template", type="string", metavar="FILE", help=u"define a template file to generate output in one call. A displayable item in the file is in the form [--datatype=TI]. The following are possible options within each item: --datatype,--ratingchar. Note that the short forms of the options are not currently supported! None of these options are applicable at command line when using templates.")
        self.parser.add_option("-d", "--datatype", dest="datatype", default="TI", type="string", metavar="DATATYPE", help=u"[default: %default] The data type options are: ST (status), CA (coverart), TI (title), AL (album), AR (artist), GE (genre), YR (year), TN (track number), FN (file name), BR (bitrate), LE (length), PP (current position in percent), PT (current position in time), VO (volume), RT (rating). Not applicable at command line when using templates.")
        self.parser.add_option("-c", "--coverartpath", dest="coverartpath", default="/tmp/cover", type="string", metavar="PATH", help=u"[default: %default] The file where coverart gets copied to if found when using the --datatype=CA option.")        
        self.parser.add_option("-r", "--ratingchar", dest="ratingchar", default="*", type="string", metavar="CHAR", help=u"[default: %default] The output character for the ratings scale. Command line option overridden if used in templates.")
        self.parser.add_option("-s", "--statustext", dest="statustext", default="Playing,Paused,Stopped", type="string", metavar="TEXT", help=u"[default: %default] The text must be comma delimited in the form 'A,B,C'. Command line option overridden if used in templates.")
        self.parser.add_option("-n", "--nounknownoutput", dest="nounknownoutput", default=False, action="store_true", help=u"Turn off unknown output such as \"Unknown\" for title and \"0:00\" for length. Command line option overridden if used in templates.")
        self.parser.add_option("-S", "--secondsoutput", dest="secondsoutput", default=False, action="store_true", help=u"Force all position and length output to be in seconds only.")
        self.parser.add_option("-m", "--maxlength", dest="maxlength", default="0", type="int", metavar="LENGTH", help=u"[default: %default] Define the maximum length of any datatypes output, if truncated the output ends in \"...\"")
        self.parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help=u"Request verbose output, not a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")                

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class MusicData:
    def __init__(self,status,coverart,title,album,length,artist,tracknumber,genre,year,filename,bitrate, current_position_percent,current_position,rating,volume):
        self.status = status
        self.coverart = coverart
        self.title = title
        self.album = album
        self.length = length
        self.artist = artist
        self.tracknumber = tracknumber
        self.genre = genre
        self.year = year
        self.filename = filename
        self.bitrate = bitrate        
        self.current_position_percent = current_position_percent
        self.current_position = current_position
        self.rating = rating
        self.volume = volume
        
class ExaileInfo:
    
    error = u""
    musicData = None
    
    def __init__(self, options):
        self.options = options
        
    def testDBus(self, bus, interface):
        obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        dbus_iface = dbus.Interface(obj, 'org.freedesktop.DBus')
        avail = dbus_iface.ListNames()
        return interface in avail
        
    def getOutputData(self, datatype, ratingchar, statustext, nounknownoutput, maxlength):
        output = u""
        
        if nounknownoutput == True:
            unknown_time = ""
            unknown_number = ""
            unknown_string = ""            
        else:
            unknown_time = "0:00"
            unknown_number = "0"
            unknown_string = "Unknown"
        
        try:
                
            bus = dbus.SessionBus()
            if self.musicData == None:
                
                if self.testDBus(bus, 'org.exaile.Exaile'):
                    
                    try:
                    
                        self.logInfo("Setting up dbus interface")
                        
                        remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
                        
                        iface = dbus.Interface(remote_object, "org.exaile.Exaile")
                        
                        self.logInfo("Calling dbus interface for music data")
                            
                        # grab the data for use
                        if iface.IsPlaying() == True:
                            status = self.getStatusText("playing", statustext)
                        else:
                            status = self.getStatusText("stopped", statustext)
                        
                        coverart = ""
                        try:                         
                            coverart = "".join(chr(byte) for byte in iface.GetCoverData())
                            # Below now done in datatype=CA section
                            #if coverart:
                            #    img = Image.open(StringIO(imgString))
                            #    img.save(self.options.coverartpath, "JPEG")
                            #    coverart = self.options.coverartpath
                        except:
                            coverart = ""
                            
                        title = iface.GetTrackAttr("title")

                        album = iface.GetTrackAttr("album")
                        
                        artist = iface.GetTrackAttr("artist")
                        
                        genre = iface.GetTrackAttr("genre")
                        
                        year = iface.GetTrackAttr("date")
                        
                        tracknumber = iface.GetTrackAttr("tracknumber")
                        
                        filename = iface.GetTrackAttr("filename")  
                        
                        bitrate = iface.GetTrackAttr("__bitrate")
                        if self.isNumeric(bitrate):
                            bitrate = str(int(bitrate)/1024)+"k/s"
                        
                        current_position_percent = iface.CurrentProgress()
                        current_position = iface.CurrentPosition()
                        
                        length = iface.GetTrackAttr('__length')
                        if self.isNumeric(length) == True and length > 0:
                            length = int(float(length))
                        else:
                            length = 0

                        if self.options.secondsoutput == True:
                            length = str(length)
                            position_parts = current_position.split(":")
                            current_position = str(int(position_parts[0])*60 + int(position_parts[1]))
                        else:
                            length = '%d:%02d' % (length / 60, length % 60)

                        
                        volume = str(int(iface.GetVolume().split(".")[0]))
                        
                        rating = iface.GetTrackAttr("__rating")
                        if self.isNumeric(rating) == False:
                            rating = 0
                        else:
                            rating = (int(float(rating)) * 5) / 100
                        
                        self.musicData = MusicData(status,coverart,title,album,length,artist,tracknumber,genre,year,filename,bitrate,current_position_percent,current_position,rating,volume)
                            
                    except Exception, e:
                        self.logError("Issue calling the dbus service:"+e.__str__())

            if self.musicData != None:
                
                self.logInfo("Preparing output for datatype:"+datatype)

                if datatype == "ST": #status
                    if self.musicData.status == None or len(self.musicData.status) == 0:
                        output = None
                    else:
                        output = self.musicData.status

                elif datatype == "CA": #coverart
                    if self.musicData.coverart == None or len(self.musicData.coverart) == 0:
                        output = None
                    else:
                        img = Image.open(StringIO(coverart))
                        img.save(self.options.coverartpath, "JPEG")
                        self.musicData.coverart = self.options.coverartpath                        
                        output = self.musicData.coverart
                            
                elif datatype == "TI": #title
                    if self.musicData.title == None or len(self.musicData.title) == 0:
                        output = None
                    else:
                        output = self.musicData.title
                        
                elif datatype == "AL": #album
                    if self.musicData.album == None or len(self.musicData.album) == 0:
                        output = None
                    else:
                        output = self.musicData.album
                        
                elif datatype == "AR": #artist
                    if self.musicData.artist == None or len(self.musicData.artist) == 0:
                        output = None
                    else:
                        output = self.musicData.artist
                        
                elif datatype == "GE": #genre
                    if self.musicData.title == genre or len(self.musicData.genre) == 0:
                        output = None
                    else:
                        output = self.musicData.genre
                        
                elif datatype == "YR": #year
                    if self.musicData.year == None or len(self.musicData.year) == 0:
                        output = None
                    else:
                        output = self.musicData.year

                elif datatype == "TN": #tracknumber
                    if self.musicData.tracknumber == None or len(self.musicData.tracknumber) == 0:
                        output = None
                    else:
                        output = self.musicData.tracknumber
                                                
                elif datatype == "FN": #filename
                    if self.musicData.filename == None or len(self.musicData.filename) == 0:
                        output = None
                    else:
                        output = self.musicData.filename

                elif datatype == "LE": # length
                    if self.musicData.length == None or len(self.musicData.length) == 0:
                        output = None
                    else:
                        output = self.musicData.length

                elif datatype == "BR": # bitrate
                    if self.musicData.bitrate == None or len(self.musicData.bitrate) == 0:
                        output = None
                    else:
                        output = self.musicData.bitrate
                                                
                elif datatype == "PP": #current position in percent
                    if self.musicData.current_position_percent == None or len(self.musicData.current_position_percent) == 0:
                        output = None
                    else:
                        output = self.musicData.current_position_percent
                        
                elif datatype == "PT": #current position in time
                    if self.musicData.current_position == None or len(self.musicData.current_position) == 0:
                        output = None
                    else:
                        output = self.musicData.current_position
                        
                elif datatype == "VO": #volume
                    if self.musicData.volume == None or len(self.musicData.volume) == 0:
                        output = None
                    else:
                        output = self.musicData.volume
                        
                elif datatype == "RT": #rating
                    if self.musicData.rating == None or self.isNumeric(self.musicData.rating) == False:
                        output = None
                    else:
                        rating = int(self.musicData.rating)
                        if rating > 0:
                            output = u"".ljust(rating,ratingchar)
                        elif rating == 0:
                            output = u""
                        else:
                            output = None
                else:
                    self.logError("Unknown datatype provided: " + datatype)
                    return u""

            if output == None or self.musicData == None:
                if datatype in ["LE","PT"]:
                    if self.options.secondsoutput == True:
                        output = unknown_number
                    else:
                        output = unknown_time
                elif datatype in ["PP","VO","YR","TN"]:
                    output = unknown_number
                elif datatype == "CA":
                    output = ""                    
                else:
                    output = unknown_string

            if maxlength > 0 and len(output) > maxlength:
                output = output[:maxlength-3]+"..."
                            
            return output
        
        except SystemExit:
            self.logError("System Exit!")
            return u""
        except Exception, e:
            traceback.print_exc()
            self.logError("Unknown error when calling getOutputText:" + e.__str__())
            return u""

    def getStatusText(self, status, statustext):
        
        if status != None:        
            statustextparts = statustext.split(",")
            
            if status == "playing":
                return statustextparts[0]
            elif status == "paused":
                return statustextparts[1]
            elif status == "stopped":
                return statustextparts[2]
            
        else:
            return status


    def getTemplateItemOutput(self, template_text):
        
        # keys to template data
        DATATYPE_KEY = "datatype"
        RATINGCHAR_KEY = "ratingchar"
        STATUSTEXT_KEY = "statustext"
        NOUNKNOWNOUTPUT_KEY = "nounknownoutput"
        MAXLENGTH_KEY = "maxlength"
        
        datatype = None
        ratingchar = self.options.ratingchar #default to command line option
        statustext = self.options.statustext #default to command line option
        nounknownoutput = self.options.nounknownoutput #default to command line option
        maxlength = self.options.maxlength #default to command line option
        
        for option in template_text.split('--'):
            if len(option) == 0 or option.isspace():
                continue
            
            # not using split here...it can't assign both key and value in one call, this should be faster
            x = option.find('=')
            if (x != -1):
                key = option[:x].strip()
                value = option[x + 1:].strip()
                if value == "":
                    value = None
            else:
                key = option.strip()
                value = None
            
            try:
                if key == DATATYPE_KEY:
                    datatype = value
                elif key == RATINGCHAR_KEY:
                    ratingchar = value
                elif key == STATUSTEXT_KEY:
                    statustext = value
                elif key == NOUNKNOWNOUTPUT_KEY:
                    nounknownoutput = True
                elif key == MAXLENGTH_KEY:
                    maxlength = int(value)                    
                else:
                    self.logError("Unknown template option: " + option)

            except (TypeError, ValueError):
                self.logError("Cannot convert option argument to number: " + option)
                return u""
                
        if datatype != None:
            return self.getOutputData(datatype, ratingchar, statustext, nounknownoutput, maxlength)
        else:
            self.logError("Template item does not have datatype defined")
            return u""


    def getOutputFromTemplate(self, template):
        output = u""
        end = False
        a = 0
        
        # a and b are indexes in the template string
        # moving from left to right the string is processed
        # b is index of the opening bracket and a of the closing bracket
        # everything between b and a is a template that needs to be parsed
        while not end:
            b = template.find('[', a)
            
            if b == -1:
                b = len(template)
                end = True
            
            # if there is something between a and b, append it straight to output
            if b > a:
                output += template[a : b]
                # check for the escape char (if we are not at the end)
                if template[b - 1] == '\\' and not end:
                    # if its there, replace it by the bracket
                    output = output[:-1] + '['
                    # skip the bracket in the input string and continue from the beginning
                    a = b + 1
                    continue
                    
            if end:
                break
            
            a = template.find(']', b)
            
            if a == -1:
                self.logError("Missing terminal bracket (]) for a template item")
                return u""
            
            # if there is some template text...
            if a > b + 1:
                output += self.getTemplateItemOutput(template[b + 1 : a])
            
            a = a + 1

        return output
    
    def writeOutput(self):

        if self.options.template != None:
            #load the file
            try:
                fileinput = codecs.open(os.path.expanduser(self.options.template), encoding='utf-8')
                template = fileinput.read()
                fileinput.close()
            except Exception, e:
                self.logError("Error loading template file: " + e.__str__())
            else:
                output = self.getOutputFromTemplate(template)
        else:
            output = self.getOutputData(self.options.datatype, self.options.ratingchar, self.options.statustext, self.options.nounknownoutput, self.options.maxlength)

        print output.encode("utf-8")

    def isNumeric(self,value):
        try:
            temp = float(value)
            return True
        except:
            return False

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
        print >> sys.stdout,"conkyExaile v.2.16"
    else:
        if options.verbose == True:
            print >> sys.stdout, "*** INITIAL OPTIONS:"
            print >> sys.stdout, "    datatype:", options.datatype
            print >> sys.stdout, "    template:", options.template
            print >> sys.stdout, "    ratingchar:", options.ratingchar
            print >> sys.stdout, "    nounknownoutput:", options.nounknownoutput
            print >> sys.stdout, "    secondsoutput:", options.secondsoutput
            print >> sys.stdout, "    maxlength:", options.maxlength
            print >> sys.stdout, "    verbose:", options.verbose
            print >> sys.stdout, "    errorlogfile:",options.errorlogfile
            print >> sys.stdout, "    infologfile:",options.infologfile
            
        exaileinfo = ExaileInfo(options)
        exaileinfo.writeOutput()
    
if __name__ == '__main__':
    main()
    sys.exit()
    
