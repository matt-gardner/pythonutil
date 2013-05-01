#!/usr/bin/env python

import urllib2

def urlopen_with_chrome(url, save_file=None):
    opener = urllib2.build_opener()
    request = urllib2.Request(url)
    request.add_header('User-Agent',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 '
            '(KHTML, like Gecko) Chrome/9.0.597.84 Safari/534.13')
    text = opener.open(request).read()
    if save_file:
        save_file.write(text)
    return text


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-u', '--url',
            dest='url',
            default='',
            help='URL to scrape')
    parser.add_option('-o', '--output-file',
            dest='save_file',
            default='',
            help='File to save the url to')
    opts, args = parser.parse_args()
    if not opts.url or not opts.save_file:
        print 'Usage: scrape.py -u [URL] -o [OUTPUTFILE]'
        exit(-1)
    outfile = open(opts.save_file, 'w')
    urlopen_with_chrome(opts.url, outfile)
    outfile.close()


# vim: et sw=4 sts=4
