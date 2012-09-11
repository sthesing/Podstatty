Podstatty is a little experiment I'm conducting with the server logs of my podcasts.
As of now, it's in a _very_ early stage, probably _very_ buggy, and it doesn't do much, at all.
It dumps the overall traffic for each file into a sqlite db, calculates complete downloads (overall traffic/filesize) and dumps the results to a csv-file.
On top of that, it's full of hard-coded settings that only apply to my own podcast, for now.

It takes files named in this scheme: access_log_YYYY-MM-DD_filtered.txt, that do only contain the URLs of GET-Requests without the domain and the traffic caused by the request. Something like this:

    /upload/filename.mp3 42234223

For me, this does the trick.

    grep 'GET /upload/' ${BaseName} | cut -d ' ' -f 7,10 | sort > ${BaseName}_filtered.txt
    
It depends on python-sqlite, Storm, Requests and Elementtree
