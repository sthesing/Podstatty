##! /usr/bin/python
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

__author__ = "Stefan Thesing <software@webdings.de>"
__version__ = "0.1_alpha"
__date__ = "Date: 2012/09/10"
__copyright__ = "Copyright (c) 2012 Stefan Thesing"
__license__ = "GPL"

from db import Db
from storm.locals import *
import sys, os, glob
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    
    settings_path = 'settings.xml'
    if len(sys.argv) > 1:
        settings_path = sys.argv[1]

    #Read Settings from xml
    tree = ET.parse(settings_path)
    root = tree.getroot()
    db_path = root.find('db_path').text
    logfiles_path = root.find('logfiles_path').text
    base_url = root.find('base_url').text
    output_file = root.find('output_file').text
    exclude = root.find("exclude")
    exclude_strings = []
    for child in exclude:
        exclude_strings.append(child.get('content'))
            
    # Check if database as specified in settings already exists
    if os.path.exists(db_path):
        print "Database exists:" + db_path
        database = create_database("sqlite:"+ db_path)
        store = Store(database)
        db = Db(store, base_url)
    else:
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        print "Creating database:" + db_path
        database = create_database("sqlite:"+ db_path)
        store = Store(database)
        store.execute("CREATE TABLE stats (id INTEGER PRIMARY KEY, \
         url VARCHAR, traffic INTEGER, date_time_string VARCHAR)")
        store.execute("CREATE TABLE filesizes (url VARCHAR PRIMARY KEY, \
         filesize INTEGER)")
        db = Db(store, base_url)
    
    # Get a list of all files in logfiles_path that match the naming
    # scheme
    filenames = glob.glob(logfiles_path + '/access_log_*filtered.txt')
    # Process each file and store the data to database
    for filename in filenames:
        print "Coming up next: " +filename
        db.add_file(filename, exclude_strings)
    # Calculate complete downloads
    tuples = db.calculate_absolute_all()
    # Dump the results into a csv file
    f = open(output_file, 'w')
    f.write('filename;number_of_downloads\n')
    for t in tuples:
        f.write(t[0] + ';' + str(t[1]) + '\n')
    f.close()
