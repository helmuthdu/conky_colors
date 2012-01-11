#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# conkySlideshow.py is a simple python script to provide a new locally stored
# image on each call based on an input file of image URLs, for use in conky.
#
#  Author: Kaivalagi
# Created: 18/02/2011
from PIL import Image, ImageDraw
from datetime import datetime
from optparse import OptionParser
import sys
import codecs
import os
import urllib2
import socket
import traceback
import random
import uuid

# cPickle is a pickle class implemented in C - so its faster
# in case its not available, use regular pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-t", "--template", dest="template", type="string", metavar="FILE", help=u"location of the template file to define the layout of output, the placeholders are [imagename], [imageurl], [imagepath], [imagewidth], [imageheight]")
        self.parser.add_option("-l", "--imagelist", dest="imagelist", type="string", metavar="FILE", help=u"location of the text file providing the image list data, strict format required of NAME;URL on each line.")
        self.parser.add_option("-i", "--index", dest="index", type="string", default="/tmp/conkySlideshow.idx", metavar="FILE", help=u"[default: %default] Location of the temp index file used to store the last image index used")
        self.parser.add_option("-o", "--output", dest="output", type="string", default="/tmp/conkySlideshow.jpg", metavar="FILE", help=u"[default: %default] Location of the file used for output")
        self.parser.add_option("-x","--maxwidth",dest="maxwidth", type="int", default=0, metavar="NUMBER", help=u"[default: %default] Output images maximum width, if zero has no effect, maxwidth overrides maxheight if both are set")        
        self.parser.add_option("-y","--maxheight",dest="maxheight", type="int", default=0, metavar="NUMBER", help=u"[default: %default] Output images maximum height, if zero has no effect, maxwidth overrides maxheight if both are set")        
        self.parser.add_option("-r", "--random", dest="random", default=False, action="store_true", help=u"Request a random image from the list rather than the next in the series")
        self.parser.add_option("-c","--connectiontimeout",dest="connectiontimeout", type="int", default=10, metavar="NUMBER", help=u"[default: %default]")        
        self.parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help=u"Request verbose output, not a good idea when running through conky!")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")                

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class SlideshowFormatter:
    
    options = None
    DELIMITER = ";"
    
    def __init__(self,options):
        
        self.options = options
        
    def writeOutput(self):
        
        try:

            # setup default timeout of 10 seconds
            socket.setdefaulttimeout(self.options.connectiontimeout)
                    
            self.logInfo("Loading templates and image list files...")
            
            output = u""
            
            # load the imagelist lines...
            if self.options.imagelist != None and os.path.exists(os.path.expanduser(self.options.imagelist)) == True:
                imagelistpath = os.path.expanduser(self.options.imagelist)
                fileinput = codecs.open(imagelistpath, encoding='utf-8')
                imagelistlines = fileinput.read().rstrip("\n").split("\n")
                fileinput.close()
            else:
                self.logError("An image list file path must be provided otherwise nothing can be displayed!")
                return

            # load the template lines...
            if self.options.template != None and os.path.exists(os.path.expanduser(self.options.template)) == True:
                templatepath = os.path.expanduser(self.options.template)
                fileinput = codecs.open(templatepath, encoding='utf-8')
                template = fileinput.read().rstrip("\n")
                fileinput.close()
            else:
                template = "[imagename]([imageurl])\n${image [imagepath] -n -p 0,0 -s 100x100}"
    
            self.logInfo("Building output for each line of text...")
            
            maximageindex = len(imagelistlines) - 1
            
            if self.options.random == True:
                # randomly pick an image
                self.logInfo("Generating random image list index to use")
                imageindex = random.randint(0, maximageindex)
                
            else:
                
                # load the last known image index used and add 1 or rest to the start
                self.logInfo("Loading image list index that was used last time")

                indexfilepath = os.path.expanduser(self.options.index)
                
                if os.path.exists(indexfilepath):
                    try:
                        self.logInfo("Loading index file " + indexfilepath)
                        file = open(indexfilepath, 'rb')
                        imageindex = pickle.load(file)
                        file.close()
                    except Exception, e:
                        self.logError("Unable to read the index file %s: %s" % (indexfilepath, e.__str__()))
                        self.logInfo("Deleting index file due to loading issues, it will be prepared again after starting the index at the beginning...")
                        os.remove(indexfilepath)
                        imageindex = maximageindex

                    if self.isNumeric(imageindex):
                        imageindex = int(imageindex)
                    else:
                        self.logError("Image list index wasn't a valid number, starting at the beginning...")
                        imageindex = maximageindex
                else:
                    self.logInfo("No image index file of %s found, starting at the beginning..."%indexfilepath)
                    imageindex = maximageindex
                    
                if imageindex < maximageindex:
                    imageindex = imageindex + 1
                else:
                    imageindex = 0

                # store new index back
                self.logInfo("Storing image list index that will be used this time")
                try:
                    self.logInfo("Saving updated index file " + indexfilepath)
                    file = open(indexfilepath, 'wb')
                    pickle.dump(imageindex, file)
                    file.close()
                except Exception, e:
                    self.logError("Unable to save index file %s: %s" % (indexfilepath, e.__str__()))
                    return False
                        
            # grab the data for the indexed image
            self.logInfo("Using imageindex of %s"%imageindex)
            imagedata = imagelistlines[imageindex].split(self.DELIMITER)
            
            imagename = imagedata[0]
            imageurl = imagedata[1]
            
            # retrieve the image via it's URL and store locally
            tempimage = "/tmp/"+str(uuid.uuid1())+self.getFilenameFromURL(imageurl)
            self.saveImageByURL(imageurl, tempimage)
            
            # resize if needed
            width, height = self.resizeImage(tempimage, self.options.maxwidth, self.options.maxheight, self.options.output)
            
            # remove temp image
            os.remove(tempimage)
            
            # generate formatted output using template
            self.logInfo("Generating formatted output using template '%s'"%template)
            output = self.getOutputFromTemplate(template, imagename, imageurl, self.options.output, width, height)
                 
            print output.encode("utf-8")
        
        except Exception, e:
            self.logError("writeOutput error:" + e.__str__())   

    def resizeImage(self, imagepath, maxwidth, maxheight, outputimagepath):
        
        img = Image.open(imagepath)
        
        width, height = img.size
        
        aspect = float(width) / float(height)
        
        if maxwidth != 0 and maxwidth < width:              
            width = int(maxwidth)
            height = int(float(maxwidth) / aspect)
        elif maxheight != 0 and maxheight < height:
            width = int(float(maxheight) * aspect)
            height = int(maxheight)
            
        newsize = (width, height)
        
        if img.size != newsize:
            self.logInfo("Resizing image to %sx%s"%(width, height))
            img.thumbnail(newsize, Image.ANTIALIAS)
        
        img.save(outputimagepath)
        
        return newsize
        
    def getFilenameFromURL(self, url):
        # get last "/" position
        startpos = url.rfind("/")
        return url[startpos+1:]
        
    def saveImageByURL(self, imageurl, imagepath):
        
        try:

            self.logInfo("Fetching image from " + imageurl)

            usock = urllib2.urlopen(imageurl)
            img = usock.read()
        except Exception, e:
            self.logError("Error downloading the image file: " + e.__str__()+"\n"+traceback.format_exc())
        else:
            # save the image and contruct an image tag
            imgfile = open(imagepath,'wb')
            imgfile.write(img)
            self.logInfo("Saved image to " + imagepath)
 
        finally:
            usock.close()
            imgfile.close()
            
    def getOutputFromTemplate(self, template, imagename, imageurl, imagepath, imagewidth, imageheight):

        try:

            output = template

            output = output.replace("[imagename]",imagename)
            
            output = output.replace("[imageurl]",imageurl)

            output = output.replace("[imagepath]",imagepath)

            output = output.replace("[imagewidth]",str(imagewidth))
            
            output = output.replace("[imageheight]",str(imageheight))
            # get rid of any excess crlf's and add just one
            output = output.rstrip(" \n")
            output = output + "\n"

            return output

        except Exception,e:
            self.logError("getOutputFromTemplate:Unexpected error:" + traceback.format_exc())
            return ""
        
    def isNumeric(self, string):
        try:
            dummy = float(string)
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
            
if __name__ == "__main__":
    
    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.verbose == True:
        print >> sys.stdout, "*** INITIAL OPTIONS:"
        print >> sys.stdout, "    template:", options.template
        print >> sys.stdout, "    imagelist:", options.imagelist
        #print >> sys.stdout, "    delimiter:", options.delimiter
        print >> sys.stdout, "    index:", options.index
        print >> sys.stdout, "    output:", options.output
        print >> sys.stdout, "    maxwidth:", options.maxwidth
        print >> sys.stdout, "    maxheight:", options.maxheight        
        print >> sys.stdout, "    random:", options.random
        print >> sys.stdout, "    connectiontimeout:", options.connectiontimeout
        print >> sys.stdout, "    verbose:", options.verbose
        print >> sys.stdout, "    errorlogfile:",options.errorlogfile
        print >> sys.stdout, "    infologfile:",options.infologfile            

    slideshowFormatter = SlideshowFormatter(options)
    slideshowFormatter.writeOutput()
    
