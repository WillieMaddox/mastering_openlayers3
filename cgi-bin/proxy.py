#!/usr/bin/env python


"""This is a blind proxy that we use to get around browser
restrictions that prevent the Javascript from loading pages not on the
same server as the Javascript.  This has several problems: it's less
efficient, it might break some sites, and it's a security risk because
people can use this proxy to browse the web and possibly do bad stuff
with it.  It only loads pages via http and https, but it can load any
content type. It supports GET and POST requests.

Copyright 2011 OpenLayers Contributors
Adapted by Gabor Farkas"""

import urllib2
import cgi
import sys, os

method = os.environ["REQUEST_METHOD"]

if not os.environ["QUERY_STRING"].startswith("http://") or not os.environ["QUERY_STRING"].startswith("https://"):
    os.environ["QUERY_STRING"] = 'http:/'+os.environ["PATH_INFO"]+'?'+os.environ["QUERY_STRING"]
if method == "POST":
    qs = os.environ["QUERY_STRING"]
    d = cgi.parse_qs(qs)
    if d.has_key("url"):
        url = d["url"][0]
    else:
        url = "http://www.openlayers.org"
else:
    fs = cgi.FieldStorage()
    url = os.environ["QUERY_STRING"]
    url = urllib2.unquote(url)

# if not url:
#     print "Content-Type: text/plain"
#     print
#     # print os.environ["REQUEST_METHOD"]
#     # print os.environ["QUERY_STRING"]
#     # print os.environ["CONTENT_TYPE"]
#     print fs
#     # print os.environ
#     # print ''.join(sorted([k+': '+v+'\n' for k, v in os.environ.iteritems()]))
#     exit()

try:
    if url.startswith("http://") or url.startswith("https://"):
        if method == "POST":
            length = int(os.environ["CONTENT_LENGTH"])
            headers = {"Content-Type": os.environ["CONTENT_TYPE"]}
            body = sys.stdin.read(length)
            r = urllib2.Request(url, body, headers)
            y = urllib2.urlopen(r)
        else:
            y = urllib2.urlopen(url)
        # print content type header
        i = y.info()
        if i.has_key("Content-Type"):
            print "Content-Type: %s" % (i["Content-Type"])
        else:
            print "Content-Type: text/plain"
        print
        print y.read()
        y.close()
    else:
        print "Content-Type: text/plain"
        print
        print "Illegal request DICKS."
except Exception, E:
    print "Status: 500 Unexpected Error"
    print "Content-Type: text/plain"
    print 
    print "Some unexpected error occurred. Error text was:", E
