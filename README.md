# Podstatty #

Podstatty is a little experiment I use to generate statistics for my podcasts from server logs.

For the Moment, it takes prepared server logs as input (see [Input](#input) for details) and spits out to files:

1. A sqlite db containing 
    - a list of traffic per episode file per day and 
    - a list of the filesizes.
2. A csv-file of complete downloads (calculated as `(overall traffic)/filesize`) per episode file

The csv file just shows a simplified count of how many times which file has been downloaded. The sqlite db can be used by other software (e.g. [GNU R](http://www.r-project.org/) to generate more elaborate statistics.

## Dependencies ##

It depends on python-sqlite, Storm, Requests and Elementtree
On a Debian-based system, you'll probably get everything you need by running `apt-get install python-sqlite python-storm python-requests python-lxml`

## Input ##

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

