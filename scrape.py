#!/usr/bin/env python

import requests

user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13'
user_agent += ' (KHTML, like Gecko) Chrome/9.0.597.84 Safari/534.13'

def urlopen_with_chrome(url, params=None, save_file=None):
    headers = {'User-Agent': user_agent}
    result = requests.get(url, params=params, headers=headers)
    text = result.text
    if save_file:
        save_file.write(text.encode('utf-8'))
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
    urlopen_with_chrome(opts.url, save_file=outfile)
    outfile.close()


# vim: et sw=4 sts=4
