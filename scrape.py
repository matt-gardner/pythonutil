#!/usr/bin/env python

import urllib2

def urlopen_with_chrome(url):
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.add_header('User-Agent',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 '
            '(KHTML, like Gecko) Chrome/9.0.597.84 Safari/534.13')
    return opener.open(request).read()


# vim: et sw=4 sts=4
