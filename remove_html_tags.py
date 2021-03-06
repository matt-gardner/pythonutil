#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def remove_html_tags(line, htmlsequences):
    newline = line
    for sequence in htmlsequences:
        newline = newline.replace(sequence, htmlsequences[sequence])
    return newline


def unicode_to_ascii(line, conversions):
    newline = line
    for sequence in conversions:
        newline = newline.replace(sequence, conversions[sequence])
    return newline


def unicode_to_latex(line, conversions):
    # This assumes the same conversion dictionary as in unicode_to_ascii,
    # so we make a few small modifications before proceeding
    conversions[u'“'] = '``'
    conversions[u'”'] = "''"
    conversions[u'‘'] = "`"
    conversions[u'’'] = "'"
    conversions[u'…'] = '\ldots '
    conversions['...'] = '\ldots '
    conversions['. . .'] = '\ldots '
    conversions[u'–'] = '---'
    conversions[u'#'] = '\#'
    newline = line
    for sequence in conversions:
        newline = newline.replace(sequence, conversions[sequence])
    return newline


def remove_comments(line):
    import re
    r = re.compile(r'<!--.*?-->')
    newline = line
    match = r.match(newline)
    while match:
        newline = newline.replace(newline[match.start():match.end()], '')
        match = r.match(newline)
    return newline


def has_html_tags(line, htmlsequences):
    for sequence in htmlsequences:
        if sequence in line:
            return True
    return False


def get_html_sequences():
    htmlsequences = dict()

    htmlsequences['&aacute;'] = u'á'
    htmlsequences['&eacute;'] = u'é'
    htmlsequences['&iacute;'] = u'í'
    htmlsequences['&oacute;'] = u'ó'
    htmlsequences['&uacute;'] = u'ú'
    htmlsequences['&ntilde;'] = u'ñ'
    htmlsequences['&agrave;'] = u'à'
    htmlsequences['&atilde;'] = u'ã'
    htmlsequences['&egrave;'] = u'è'
    htmlsequences['&oslash;'] = u'ø'
    htmlsequences['&ccedil;'] = u'ç'
    htmlsequences['&Aring;'] = u'Å'
    htmlsequences['&acirc;'] = u'â'
    htmlsequences['&ocirc;'] = u'ô'
    htmlsequences['&aelig;'] = u'æ'
    htmlsequences['&auml;'] = u'ä'
    htmlsequences['&iuml;'] = u'ï'
    htmlsequences['&ouml;'] = u'ö'
    htmlsequences['&uuml;'] = u'ü'
    htmlsequences['&iquest;'] = u'¿'
    htmlsequences['&copy;'] = u'©'
    htmlsequences['&reg;'] = u'®'
    htmlsequences['&quot;'] = u'"'
    htmlsequences['&cent;'] = u'¢'
    htmlsequences['&trade;'] = u'™'
    htmlsequences['&gt;'] = u'>'
    htmlsequences['&lt;'] = u'<'
    htmlsequences['&ldquo;'] = u'“'
    htmlsequences['&rdquo;'] = u'”'
    htmlsequences['&lsquo;'] = u'‘'
    htmlsequences['&rsquo;'] = u'’'
    htmlsequences['&nbsp;'] = u' '
    htmlsequences['&amp;'] = u'&'
    htmlsequences['&ndash;'] = u'–'
    htmlsequences['&dash;'] = u'-'
    htmlsequences['&hellip;'] = u'…'
    htmlsequences['&bull;'] = u'•'
    htmlsequences['&lsqb;'] = u'['
    htmlsequences['&rsqb;'] = u']'
    htmlsequences['&mdash;'] = u'\u2014'
    htmlsequences['&shy;'] = u'\u2013'
    htmlsequences['&breve;'] = u'\u0306'
    htmlsequences['&dagger;'] = u'\u2020'
    htmlsequences['&macr;'] = u'\u0304'
    htmlsequences['&lpar;'] = u'('
    htmlsequences['&rpar;'] = u')'
    htmlsequences['&ast;'] = u'*'
    htmlsequences['&quest;'] = u'?'
    htmlsequences['&ulcrop;'] = u'\u230f'
    htmlsequences['&urcrop;'] = u'\u230e'
    htmlsequences['&verbar;'] = u'|'
    # I don't know what these sequences are, but they are here so I can ignore
    # them in another program I'm writing
    #htmlsequences['&open;'] = u''
    #htmlsequences['&close;'] = u''
    #htmlsequences['&top;'] = u''
    #htmlsequences['&dot;'] = u''
    #htmlsequences['&ldsqb;'] = u''
    #htmlsequences['&rdsqb;'] = u''
    #htmlsequences['&lang;'] = u''
    #htmlsequences['&num;'] = u''
    #htmlsequences['&rpress;'] = u''
    #htmlsequences['&lpress;'] = u''
    #htmlsequences['&stigma;'] = u''

    htmlsequences['&#039;'] = u"'"
    htmlsequences['&#91;'] = u'['
    htmlsequences['&#133;'] = u'…'
    htmlsequences['&#146;'] = u'’'
    htmlsequences['&#147;'] = u'“'
    htmlsequences['&#148;'] = u'”'
    htmlsequences['&#150;'] = u'–'
    htmlsequences['&#151;'] = u'—'
    htmlsequences['&#163;'] = u'£'
    htmlsequences['&#169;'] = u'©'
    htmlsequences['&#176;'] = u'°'
    htmlsequences['&#177;'] = u'±'
    htmlsequences['&#225;'] = u'á'
    htmlsequences['&#228;'] = u'ä'
    htmlsequences['&#233;'] = u'é'
    htmlsequences['&#241;'] = u'ñ'
    htmlsequences['&#243;'] = u'ó'
    htmlsequences['&#246;'] = u'ö'
    htmlsequences['&#249;'] = u'ù'
    htmlsequences['&#250;'] = u'ú'

    return htmlsequences


def get_unicode_conversions():
    conversions = dict()
    conversions[u'Å'] = 'A'
    conversions[u'á'] = 'a'
    conversions[u'à'] = 'a'
    conversions[u'ã'] = 'a'
    conversions[u'â'] = 'a'
    conversions[u'ä'] = 'a'
    conversions[u'æ'] = 'ae'
    conversions[u'é'] = 'e'
    conversions[u'è'] = 'e'
    conversions[u'í'] = 'i'
    conversions[u'ï'] = 'i'
    conversions[u'ó'] = 'o'
    conversions[u'ô'] = 'o'
    conversions[u'ö'] = 'o'
    conversions[u'ø'] = 'o'
    conversions[u'ú'] = 'u'
    conversions[u'ù'] = 'u'
    conversions[u'ü'] = 'u'
    conversions[u'ç'] = 'c'
    conversions[u'ñ'] = 'n'
    conversions[u'“'] = '"'
    conversions[u'”'] = '"'
    conversions[u'‘'] = "'"
    conversions[u'’'] = "'"
    conversions[u'–'] = '-'
    conversions[u'—'] = '-'
    conversions[u'¿'] = ''
    conversions[u'…'] = '...'
    conversions[u'•'] = ''
    conversions[u'£'] = ''
    conversions[u'°'] = ''
    conversions[u'±'] = ''
    conversions[u'©'] = ''
    conversions[u'®'] = ''
    conversions[u'¢'] = ''
    conversions[u'™'] = ' TM '
    conversions[u'\ufb01'] = 'fi'
    conversions[u'\xde'] = 'fi'
    conversions[u'\ufb02'] = 'fl'
    conversions[u'\xdf'] = 'fl'
    # This is a bullet point, or is supposed to be
    conversions[u'\xa5'] = ' - '
    conversions[u'\u2014'] = '-'
    conversions[u'\u0306'] = ''
    conversions[u'\u2020'] = ''
    conversions[u'\u2029'] = '\n\n'
    conversions[u'\u0304'] = ''
    conversions[u'\u230f'] = ''
    conversions[u'\u230e'] = ''
    conversions[u'\xa0'] = ' '
    conversions[u'\xca'] = ' '
    return conversions


# vim: et sw=4 sts=4
