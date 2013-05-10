Podstatty is a little experiment I'm conducting with the server logs of my podcasts.
As of now, it's in a _very_ early stage, probably _very_ buggy, and it doesn't do much, at all.
It dumps the overall traffic for each file into a sqlite db, calculates complete downloads (overall traffic/filesize) and dumps the results to a csv-file.

It depends on python-sqlite, Storm, Requests and Elementtree

# Input #

Download the logfile you want to process. Podstatty takes files named in this scheme: access_log_YYYY-MM-DD_filtered.txt, that do only contain the URLs of GET-Requests without the domain and the traffic caused by the request. Something like this:

    /upload/filename.mp3 42234223

For me, this does the trick.

    grep 'GET /upload/' ${BaseName} | cut -d ' ' -f 7,10 | sort > ${BaseName}_filtered.txt

See `filter_stats.sh` for the shell script I use to prepare my logfiles. Maybe you can work from there.

# Usage #
If you have your logfiles in the specified format, you need to prepare the `settings.xml` file. If you only have one podcast, you only *need* to set the `base_url` and `logfiles_path`, values. You can leave the others with example data.

Per default, podstatty uses the `settings.xml` file. It can be run using:

    python podstatty.py

If you have more than one podcast, you can make one copy of your `settings.xml` file per podcast containing specific settings, e.g. `podcast1.xml` and `podcast2.xml`. In that case you want to modify all the fields in the respective settings file. You then run:

    python podstatty.py podcast1.xml

# Bug Warning #
I seem to have a big bug in here, probably when determining the filesizes. You should probably double check those in the respective database table and correct them manually.  
Furthermore, I'd be thankful for any help in tracking down that bug. 


