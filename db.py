# -*- coding: utf8 -*-
##This file is part of Podstatty.
##
##Podstatty is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##Podstatty is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with Podstatty. If not, see http://www.gnu.org/licenses/.

from storm.locals import Storm, Int, Unicode, ReferenceSet
import requests

class Stats(Storm):
    """
    The table containing the actual numbers 
    'CREATE TABLE stats (id INTEGER PRIMARY KEY, url VARCHAR, 
    traffic INTEGER, date_time_string VARCHAR)'
    """
    __storm_table__ = "stats"
    id = Int(primary=True)
    url = Unicode()
    traffic = Int()
    date_time_string = Unicode()
    
    
    def __init__(self, url, traffic, date_time_string):
        self.url = url
        self.traffic = traffic
        self.date_time_string = date_time_string
        
class Filesizes(Storm):
    """
    The table containing the filesizes for each URL
    'CREATE TABLE filesizes (url VARCHAR PRIMARY KEY, filesize INTEGER)'
    """
    __storm_table__ = "filesizes"
    url = Unicode(primary=True)
    filesize = Int()
    
    def __init__(self, url, filesize):
        self.url = url
        self.filesize = filesize
        
class Db:
    def __init__(self, store, base_url):
        self.store = store
        self.base_url = base_url

    def add_file(self, filename):
        log = open(filename)
        date = filename.split("access_log_")[1]
        date = date.replace("_filtered.txt", "")
        if self.store.find(Stats, Stats.date_time_string == unicode(date)).count():
            print "A logfile for this date has already been processed."
            return None
        stats =[]
        for line in log:
            if (not "torrent" in line) and (not "-\n" in line) :
                split_line = line.split()
                stat = Stats(unicode(split_line[0]), int(split_line[1]), unicode(date))
                stats.append(stat)
        urls = []
        for stat in stats:
            if not stat.url in urls:
                urls.append(stat.url)
        for url in urls:
            new_stat = Stats(url, 0, unicode(date))
            for stat in stats:
                if stat.url == url:
                    new_stat.traffic = new_stat.traffic+stat.traffic
            self.store.add(new_stat)
            #check if all URLs are already in table "filesizes", if not,
            #get the filesize and write it into that table
            self.check_url(url)
        
        self.store.flush()
        self.store.commit()

    def check_url(self, url):
        #if the url is not yet in this table
        if not self.store.find(Filesizes, Filesizes.url == url).count():
            # Get the filesize from the server
            # TODO Implement error routine
            r = requests.head(self.base_url + url)
            size = int(r.headers['Content-Length'])
            # Write the URL and it's filesize to database 
            self.store.add(Filesizes(url, size))
            
            
