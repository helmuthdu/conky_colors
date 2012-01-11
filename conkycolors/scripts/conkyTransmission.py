#!/usr/bin/python2
# -*- coding: utf-8 -*-
###############################################################################
# conkyTransmission.py is a simple python script to gather
# details of Deluge torrents for use in conky.
#
# Author: Kaivalagi
# Created: 13/10/2008
#
#Modified:

from datetime import datetime
import transmissionrpc
from optparse import OptionParser
import codecs
import logging
import os
import sys

class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-s","--server", dest="server", type="string", default="127.0.0.1", metavar="SERVER", help=u"[default: %default] The server to connect to where the transmission daemon is running")
        self.parser.add_option("-p","--port", dest="port", type="int", default=9091, metavar="PORT", help=u"[default: %default] The port to connect to where the transmission daemon is running")
        self.parser.add_option("-U","--username", dest="username", type="string", default="", metavar="USERNAME", help=u"[default: %default] Username to use when connecting")
        self.parser.add_option("-P","--password", dest="password", type="string", default="", metavar="PASSWORD", help=u"[default: %default] Password to use when connecting")        
        self.parser.add_option("-S","--showsummary",dest="showsummary", default=False, action="store_true", help=u"Display summary output. This is affected by the --activeonly option.")
        self.parser.add_option("-H","--hidetorrentdetail",dest="hidetorrentdetail", default=False, action="store_true", help=u"Hide torrent detail output, if used no torrent details are output.")
        self.parser.add_option("-t","--torrenttemplate",dest="torrenttemplate", type="string", metavar="FILE", help=u"Template file determining the format for each torrent. Use the following placeholders: [name], [state], [totaldone], [totalsize], [progress], [nofiles], [downloadrate], [uploadrate], [eta], [currentpeers], [currentseeds], [totalpeers], [totalseeds], [ratio].")
        self.parser.add_option("-T","--summarytemplate",dest="summarytemplate", type="string", metavar="FILE", help=u"Template file determining the format for summary output. Use the following placeholders: [notorrents], [totalprogress], [totaldone], [totalsize], [totaldownloadrate], [totaluploadrate], [totaleta], [currentpeers], [currentseeds], [totalpeers], [totalseeds], [totalratio].")
        self.parser.add_option("-a", "--activeonly", dest="activeonly", default=False, action="store_true", help=u"If set only info for torrents in an active state will be displayed.")
        self.parser.add_option("-l","--limit",dest="limit", default=0, type="int", metavar="NUMBER", help=u"[default: %default] Define the maximum number of torrents to display, zero means no limit.")
        self.parser.add_option("-w","--maxwidth",dest="maxwidth", default=0, type="int", metavar="CHARS", help=u"[default: %default] Define the maximum number of characters for name output, zero means no limit.")
        self.parser.add_option("-b","--sortby",dest="sortby", default="eta", type="string", metavar="SORTTYPE", help=u"Define the sort method for output, can be \"progress\", \"queue\", \"eta\", \"download\", \"upload\" and \"ratio\". Also note that a torrent's state supersedes anything else for sorting, in the order, from top to bottom: downloading, seeding, queued, paused, unknown)")
        self.parser.add_option("-v","--verbose",dest="verbose", default=False, action="store_true", help=u"Request verbose output, no a good idea when running through conky!")
        self.parser.add_option("-V", "--version", dest="version", default=False, action="store_true", help=u"Displays the version of the script.")
        self.parser.add_option("--errorlogfile", dest="errorlogfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends errors to the filepath.")
        self.parser.add_option("--infologfile", dest="infologfile", type="string", metavar="FILE", help=u"If a filepath is set, the script appends info to the filepath.")

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

    def print_help(self):
        return self.parser.print_help()

class TorrentData:

    def __init__(self, name, state, statecode, totaldone, totalsize, progress, nofiles, downloadrate, downloadtext, uploadrate, uploadtext, eta, etatext, currentpeers, currentseeds, totalpeers, totalseeds, ratio, queueorder, sortby):
        self.name = name
        self.state = state
        self.statecode = statecode
        self.totaldone = totaldone
        self.totalsize = totalsize
        self.progress = progress
        self.nofiles = nofiles
        self.downloadrate = downloadrate
        self.downloadtext = downloadtext
        self.uploadrate = uploadrate
        self.uploadtext = uploadtext
        self.eta = eta
        self.etatext = etatext
        self.currentpeers = currentpeers
        self.currentseeds = currentseeds
        self.totalpeers = totalpeers
        self.totalseeds = totalseeds
        self.ratio = ratio
        self.queueorder = queueorder
        self.sortby = sortby

    def __cmp__(self, other):
        if self.sortby == "progress":
            return cmp(self.getProgressOrder(self.statecode,self.progress) , self.getProgressOrder(other.statecode,other.progress))
        elif self.sortby == "queue":
            return cmp(self.getQueueOrder(self.statecode,self.queueorder) , self.getQueueOrder(other.statecode,other.queueorder))
        elif self.sortby == "eta":
            return cmp(self.getETAOrder(self.statecode,self.eta) , self.getETAOrder(other.statecode,other.eta))
        elif self.sortby == "download":
            return cmp(self.getRateOrder(self.statecode,self.downloadrate) , self.getRateOrder(other.statecode,other.downloadrate))
        elif self.sortby == "upload":
            return cmp(self.getRateOrder(self.statecode,self.uploadrate) , self.getRateOrder(other.statecode,other.uploadrate))
        elif self.sortby == "ratio":
            return cmp(self.getRatioOrder(self.statecode,self.ratio) , self.getRatioOrder(other.statecode,other.ratio))
        else:
            return 0

    def __str__(self):
        return str(self.name + " - " + self.eta)

    def getProgressOrder(self,statecode,progress):
        return (statecode*10000.0)+float(progress.rstrip("%"))

    def getQueueOrder(self,statecode,queueorder):
        if queueorder <> -1:
            queueorder = 1000 - queueorder
        return (statecode*10000.0)+float(queueorder)

    def getETAOrder(self,statecode,eta):
        try:
            if eta <> -1:
                eta = (100000000 - eta)/100
            return (statecode*10000000.0)+float(eta)
        except:
            return 0

    def getRateOrder(self,statecode,rate):
        try:
            return (statecode*1000000.0)+float(rate)
        except:
            return 0

    def getRatioOrder(self,statecode,ratio):
        try:
            return (statecode*10000.0)+(100.0*float(ratio))
        except:
            return 0

class TransmissionInfo:

    uri = None
    options = None
    sessionstate = None
    sessionstatefound = False

    STATE_DOWNLOADING = 4
    STATE_SEEDING = 3
    STATE_QUEUED = 2
    STATE_PAUSED = 1
    STATE_UNKNOWN = 0
        
    def __init__(self, options):

        try:

            #disable all logging within Deluge functions, only output info from this script
            logging.disable(logging.FATAL)

            self.options = options

            # sort out the server option
            self.options.server = self.options.server.replace("localhost", "127.0.0.1")

            # create the rpc and client objects
            self.client = transmissionrpc.Client(self.options.server, self.options.port) #, self.options.username, self.options.password)

        except Exception,e:
            self.logError("TransmissionInfo Init:Unexpected error:" + e.__str__())

    def getTorrentTemplateOutput(self, template, name, state, totaldone, totalsize, progress, nofiles, downloadrate, uploadrate, eta, currentpeers, currentseeds, totalpeers, totalseeds, ratio):

        try:

            output = template

            output = output.replace("[name]",name)
            output = output.replace("[state]",state)
            output = output.replace("[totaldone]",totaldone)
            output = output.replace("[totalsize]",totalsize)
            output = output.replace("[progress]",progress)
            output = output.replace("[nofiles]",nofiles)
            output = output.replace("[downloadrate]",downloadrate)
            output = output.replace("[uploadrate]",uploadrate)
            output = output.replace("[eta]",eta)
            output = output.replace("[currentpeers]",currentpeers)
            output = output.replace("[currentseeds]",currentseeds)
            output = output.replace("[totalpeers]",totalpeers)
            output = output.replace("[totalseeds]",totalseeds)
            output = output.replace("[ratio]",ratio)

            # get rid of any excess crlf's and add just one
            output = output.rstrip(" \n")
            output = output + "\n"

            return output

        except Exception,e:
            self.logError("getTorrentTemplateOutput:Unexpected error:" + e.__str__())
            return ""

    def getSummaryTemplateOutput(self, template, notorrents, totalprogress, totaldone, totalsize, totaldownloadrate, totaluploadrate, totaleta, currentpeers, currentseeds, totalpeers, totalseeds, totalratio):

        try:

            output = template

            output = output.replace("[notorrents]",notorrents)
            output = output.replace("[totalprogress]",totalprogress)
            output = output.replace("[totaldone]",totaldone)
            output = output.replace("[totalsize]",totalsize)
            output = output.replace("[totaldownloadrate]",totaldownloadrate)
            output = output.replace("[totaluploadrate]",totaluploadrate)
            output = output.replace("[totaleta]",totaleta)
            output = output.replace("[currentpeers]",currentpeers)
            output = output.replace("[currentseeds]",currentseeds)
            output = output.replace("[totalpeers]",totalpeers)
            output = output.replace("[totalseeds]",totalseeds)
            output = output.replace("[totalratio]",totalratio)

            # get rid of any excess crlf's and add just one
            output = output.rstrip(" \n")
            output = output + "\n"

            return output

        except Exception,e:
            self.logError("getSummaryTemplateOutput:Unexpected error:" + e.__str__())
            return ""

    def writeOutput(self):

        try:

            self.logInfo("Proceeding with torrent data interpretation...")

            torrentDataList = []
            torrentItemList = ["num_peers","num_seeds","name","state","total_done","total_size","total_wanted","progress","files","eta","download_payload_rate","upload_payload_rate","total_peers","total_seeds","ratio","queue"]
            highesteta = 0

            # summary variables
            summary_notorrent = 0
            summary_totaldone = 0
            summary_totalsize = 0
            summary_totaldownloadrate = 0.0
            summary_totaluploadrate = 0.0
            summary_totaleta = 0
            summary_currentpeers = 0
            summary_currentseeds = 0
            summary_totalpeers = 0
            summary_totalseeds = 0
            summary_totalratio = 0.0

            self.logInfo("Preparing templates...")

            if self.options.summarytemplate == None:
                # create default summary template
                summarytemplate = "Total Torrents Queued:[notorrents] \n[totaldone]/[totalsize] - [totalprogress]\n" + "DL: [totaldownloadrate] UL: [totaluploadrate]\n"
            else:
                # load the template file contents
                try:
                    #fileinput = open(self.options.summarytemplate)
                    fileinput = codecs.open(os.path.expanduser(self.options.summarytemplate), encoding='utf-8')
                    summarytemplate = fileinput.read()
                    fileinput.close()
                except:
                    self.logError("Summary Template file no found!")
                    sys.exit(2)

            if self.options.torrenttemplate == None:
                # create default template
                torrenttemplate = "[name]\n[state]\n[totaldone]/[totalsize] - [progress]\n" + "DL: [downloadrate] UL: [uploadrate] ETA:[eta]\n"
            else:
                # load the template file contents
                try:
                    #fileinput = open(self.options.torrenttemplate)
                    fileinput = codecs.open(os.path.expanduser(self.options.torrenttemplate), encoding='utf-8')
                    torrenttemplate = fileinput.read()
                    fileinput.close()
                except:
                    self.logError("Torrent Template file no found!")
                    sys.exit(2)

            self.torrents = self.client.list()
            if len(self.torrents) > 0:

                self.logInfo("Processing %s torrent(s)..."%str(len(self.torrents)))

                for torrentid, torrent in self.torrents.iteritems():

                    if torrent != None:

                        if self.options.activeonly == True:

                            if torrent.status == "downloading" or torrent.status == "seeding":
                                active = True
                            else:
                                active = False
                                 
                            #active = False

                            # check for activity
                            #if "num_peers" in torrent.fields:
                            #    if torrent.fields["num_peers"] > 0:
                            #        active = True

                            #if "num_seeds" in torrent.fields:
                            #    if torrent.fields["num_seeds"] > 0:
                            #        active = True

                        # output details if all required or if active
                        if self.options.activeonly == False or active == True:

                            name = torrent.name
                            if self.options.maxwidth > 0:
                                name = name[:self.options.maxwidth]

                            if "status" in torrent.fields:
                                statecode = torrent.fields["status"]
                            else:
                                statecode = self.STATE_UNKNOWN
                                
                            state = torrent.status.title()

                            if "downloadedEver" in torrent.fields:
                                totaldone = self.fsize(torrent.fields["downloadedEver"])
                                summary_totaldone = summary_totaldone + int(torrent.fields["downloadedEver"])
                            else:
                                totaldone = "??.? KiB"

                            if "sizeWhenDone" in torrent.fields:
                                totalsize = self.fsize(torrent.fields["sizeWhenDone"])
                                summary_totalsize = summary_totalsize + int(torrent.fields["sizeWhenDone"])
                            else:
                                totalsize = "??.? KiB"
                                
                            progress = str(round(torrent.progress,2))+"%"

                            nofiles = str(len(torrent.files()))


                            if torrent.eta != None:
                                eta = torrent.eta.seconds
                            else:
                                eta = -1
                                
                            if eta > highesteta:
                                highesteta = eta

                            if eta == -1:
                                etatext = "Not Available"
                            elif eta == -2:
                                etatext = "Unknown"
                            else:
                                etatext = torrent.format_eta().title()


                            if "rateDownload" in torrent.fields:
                                downloadrate = float(torrent.fields["rateDownload"])
                                summary_totaldownloadrate = summary_totaldownloadrate + downloadrate
                                downloadtext = self.fspeed(downloadrate)
                            else:
                                downloadrate = 0
                                downloadtext = "?.? KiB/s"

                            if "rateUpload" in torrent.fields:
                                uploadrate = float(torrent.fields["rateUpload"])
                                summary_totaluploadrate = summary_totaluploadrate + uploadrate
                                uploadtext = self.fspeed(uploadrate)
                            else:
                                uploadrate = 0
                                uploadtext = "?.? KiB/s"

                            #if "num_peers" in torrent.fields:
                            #    currentpeers = str(torrent.fields["num_peers"])
                            #    summary_currentpeers = summary_currentpeers + int(torrent.fields["num_peers"])
                            #else:
                            #    currentpeers = "?"
                            currentpeers = "?"
                            
                            #if "num_seeds" in torrent.fields:
                            #    currentseeds = str(torrent.fields["num_seeds"])
                            #    summary_currentseeds = summary_currentseeds + int(torrent.fields["num_seeds"])
                            #else:
                            #    currentseeds = "?"
                            currentseeds = "?"

                            #if "total_peers" in torrent.fields:
                            #    totalpeers = str(torrent.fields["total_peers"])
                            #    summary_totalpeers = summary_totalpeers + int(torrent.fields["total_peers"])
                            #else:
                            #    totalpeers = "?"
                            totalpeers = "?"

                            #if "total_seeds" in torrent.fields:
                            #    totalseeds = str(torrent.fields["total_seeds"])
                            #    summary_totalseeds = summary_totalseeds + int(torrent.fields["total_seeds"])
                            #else:
                            #    totalseeds = "?"
                            totalseeds = "?"

                            #if "ratio" in torrent.fields:
                            #    ratio = str(round(torrent.fields["ratio"],3)).ljust(5,"0")
                            #else:
                            #    ratio = "?.???"
                            ratio = str(round(torrent.ratio,2))
                            
                            # for sorting in the same way as progress, we need to order from high to low
                            #if "queue" in torrent.fields:
                            #    queueorder = torrent.fields["queue"]
                            #else:
                            #    queueorder = -1
                            queueorder = -1
                            
                            sortby = self.options.sortby

                            summary_notorrent = summary_notorrent + 1

                            # add torrent data to list
                            torrentData = TorrentData(name, state, statecode, totaldone, totalsize, progress, nofiles, downloadrate, downloadtext, uploadrate, uploadtext, eta, etatext, currentpeers, currentseeds, totalpeers, totalseeds, ratio, queueorder, sortby)
                            torrentDataList.append(torrentData)

                    else:
                        self.logInfo("No torrent status data available for torrentid: "+torrentid)

                if summary_notorrent > 0:

                    output = u""

                    if self.options.showsummary == True:

                        # sort out summary data for output
                        summary_notorrent = str(summary_notorrent)
                        summary_totalprogress = str(round((float(summary_totaldone) / float(summary_totalsize)) *100,2))+"%"
                        summary_totaldone = self.fsize(summary_totaldone)
                        summary_totalsize = self.fsize(summary_totalsize)
                        summary_totaldownloadrate = self.fspeed(summary_totaldownloadrate)
                        summary_totaluploadrate = self.fspeed(summary_totaluploadrate)
                        summary_totaleta = self.ftime(highesteta)
                        summary_currentpeers = str(summary_currentpeers)
                        summary_currentseeds = str(summary_currentseeds)
                        summary_totalpeers = str(summary_totalpeers)
                        summary_totalseeds = str(summary_totalseeds)
                        summary_totalratio = "?.???"

                        output = self.getSummaryTemplateOutput(summarytemplate, summary_notorrent, summary_totalprogress, summary_totaldone, summary_totalsize, summary_totaldownloadrate, summary_totaluploadrate, summary_totaleta, summary_currentpeers, summary_currentseeds, summary_totalpeers, summary_totalseeds, summary_totalratio)
                        output =  output.encode("utf-8")

                    if self.options.hidetorrentdetail == False:

                        outputCount = 0

                        # sort list, eta based
                        self.logInfo("Sorting torrent list using: %s"%self.options.sortby)
                        torrentDataList.sort(reverse = True)

                        # output torrent data using the template
                        for torrentData in torrentDataList:

                            # keep a tally of torrent output, if past the limit then exit
                            if self.options.limit <> 0:
                                outputCount = outputCount + 1
                                if outputCount > self.options.limit:
                                    break

                            output = output + self.getTorrentTemplateOutput(torrenttemplate, torrentData.name, torrentData.state, torrentData.totaldone, torrentData.totalsize, torrentData.progress, torrentData.nofiles, torrentData.downloadtext, torrentData.uploadtext, torrentData.etatext, torrentData.currentpeers, torrentData.currentseeds, torrentData.totalpeers, torrentData.totalseeds, torrentData.ratio)+"\n"

                    print output.encode("utf-8")

                else:
                    self.logInfo("No torrent info to display")

            else:
                self.logInfo("No torrents found")

        except Exception,e:
            self.logError("writeOutput:Unexpected error:" + e.__str__())

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
   
    def fsize(self, size):
        return self.getSizeString(size)

    def fspeed(self, speed):
        return self.getSizeString(speed, "/s")

    def ftime(self, seconds):
        return self.getTimeString(seconds)

    def getSizeString(self, bytes, suffix=""):     
        size = float(bytes)
        count = 0
        while 1:
            if len(str(int(size))) < 4 or count > 2:
                break            
            size = size / 1024
            count = count + 1
        
        # convert to string and add units
        size = str(round(size,2))
        if count == 0:
            size = size+"B"
        elif count == 1:
            size = size+"KB"
        elif count == 2:
            size = size+"MB"
        else:
            size = size+"GB"
        
        return size+suffix

    def getTimeString(self,seconds):
        time = int(seconds)
        weeks, time = divmod(time, 60*60*24*7)
        days, time = divmod(time, 60*60*24)
        hours, time = divmod(time, 60*60)
        minutes, seconds = divmod(time, 60)
        
        output = ""
        if weeks > 0:
            output = output+str(weeks)+"w "
        if days > 0:
            output = output+str(days)+"d "
        if hours > 0  and weeks == 0:
            output = output+str(hours)+"h "
        if minutes > 0 and (weeks == 0 and days == 0):
            output = output+str(minutes)+"m "
        if  weeks == 0 and days == 0 and hours == 0:
            output = output+str(seconds)+"s"
        
        return output
     
def main():

    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    if options.version == True:

        print >> sys.stdout,"conkyTransmission v.1.03"

    else:

        if options.verbose == True:
            print >> sys.stdout, "*** INITIAL OPTIONS:"
            print >> sys.stdout, "    server:",options.server
            print >> sys.stdout, "    port:",options.port
            print >> sys.stdout, "    showsummary:",options.showsummary
            print >> sys.stdout, "    torrenttemplate:",options.torrenttemplate
            print >> sys.stdout, "    summarytemplate:",options.summarytemplate
            print >> sys.stdout, "    activeonly:",options.activeonly
            print >> sys.stdout, "    limit:",options.limit
            print >> sys.stdout, "    maxwidth:",options.maxwidth
            print >> sys.stdout, "    sortby:",options.sortby
            print >> sys.stdout, "    errorlogfile:",options.errorlogfile
            print >> sys.stdout, "    infologfile:",options.infologfile

        transmissionInfo = TransmissionInfo(options)
        transmissionInfo.writeOutput()

if __name__ == '__main__':
    main()
    sys.exit()

