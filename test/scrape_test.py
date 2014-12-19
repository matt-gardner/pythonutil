#!/usr/bin/env python

from scrape import urlopen_with_chrome

def get_definition_from_pons(word):
    # TODO: get more than just the definition, get the morphology too, put it
    # into a more complex object.
    # Also keep the URL, for easy access
    definition = ''
    url = 'http://en.pons.eu/dict/search/results/?q=%s&l=ensl&in=&lf=en' % (
            word)
    print 'Querying pons with url:', url
    html = urlopen_with_chrome(url.encode('utf-8'))
    soup = BeautifulSoup(html)
    senses = []
    for sense in soup.findAll('span', attrs={'class':'sense'}):
        if sense.parent.name == 'th':
            table = sense.parent.parent.parent.parent
        else:
            table = sense.parent.parent.parent
        senses.append((sense, table))
    for sense, table in senses:
        definition += ''.join(sense.parent.findAll(text=True)).strip() + '\n'
        for target in table.findAll('td', attrs={'class':'target'}):
            source = target.findPreviousSibling('td', attrs={'class': 'source'})
            definition += ''.join(source.findAll(text=True)).strip() + ' : '
            definition += ''.join(target.findAll(text=True)).strip() + '\n'
        definition += '\n'
    if not senses:
        for target in soup.findAll('td', attrs={'class':'target'}):
            source = target.findPreviousSibling('td', attrs={'class': 'source'})
            definition += ''.join(source.findAll(text=True)).strip() + ' : '
            definition += ''.join(target.findAll(text=True)).strip() + '\n'
    return definition.strip()


if __name__ == '__main__':
    import sys
    get_definition_from_pons(sys.argv[1])


# vim: et sw=4 sts=4
