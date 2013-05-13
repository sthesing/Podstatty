# -*- coding: utf8 -*-
## Copyright (c) 2012 Stefan Thesing
##
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

import os, glob
from db import Filesizes, Stats

class Op:
    """
    A class doing the actual data processing.
    """
    def __init__(self, db):
        self.db = db

    def process_files(self, logfiles_path, exclude_strings):
        #Get a list of all files in logfiles_path that match the naming
        # scheme
        filenames = glob.glob(logfiles_path + '/access_log_*filtered.txt')
        # Process each file and store the data to database
        for filename in filenames:
            print "Coming up next: " +filename
            self.db.add_file(filename, exclude_strings)
    
    def dump_absoluste_all_to_csv(self, output_file):
        # Calculate complete downloads
        tuples = self.calculate_absolute_all()
        # Dump the results into a csv file
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        f = open(output_file, 'w')
        f.write('filename;number_of_downloads\n')
        for t in tuples:
            f.write(t[0] + ';' + str(t[1]) + '\n')
        f.close()

    def calculate_absolute_all(self):
        tuples = []
        # Get all urls
        urls = self.db.store.find(Filesizes.url)
        for url in urls:
            tuples.append(self.calculate_absolute(url))
        return tuples
    
    def calculate_absolute(self, url):
        # Get all the traffic for this url
        traffic = self.db.store.find(Stats.traffic, Stats.url == url)
        # add it up
        absolute_download = 0
        for dl in traffic:
            absolute_download = absolute_download + dl
        # Get the filesize
        filesize = self.db.store.find(Filesizes.filesize, Filesizes.url == url).one()
        # Calculate complete downloads
        # I use floor division because I want to truncate after the  
        # decimal point. In Python 2.x this doesn't make a difference,
        # but in Python 3, it does.
        complete_downloads = absolute_download//filesize
        return [url, complete_downloads]
