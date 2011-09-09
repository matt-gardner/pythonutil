#!/usr/bin/env python

greek_letters = {
        'alpha' : u'\u03b1',
        'beta' : u'\u03b2',
        'gamma' : u'\u03b3',
        'delta' : u'\u03b4',
        'epsilon' : u'\u03b5',
        'zeta' : u'\u03b6',
        'eta' : u'\u03b7',
        'theta' : u'\u03b8',
        'iota' : u'\u03b9',
        'kappa' : u'\u03ba',
        'lambda' : u'\u03bb',
        'mu' : u'\u03bc',
        'nu' : u'\u03bd',
        'ksi' : u'\u03be',
        'omicron' : u'\u03bf',
        'pi' : u'\u03c0',
        'rho' : u'\u03c1',
        'sigma_end' : u'\u03c2',
        'sigma' : u'\u03c3',
        #'lunate_sigma' : u'\u03f2', use unicodedata.normalize('NFKC') to
        # change a lunate_sigma to a sigma_end
        'tau' : u'\u03c4',
        'upsilon' : u'\u03c5',
        'phi' : u'\u03c6',
        'chi' : u'\u03c7',
        'psi' : u'\u03c8',
        'omega' : u'\u03c9',
        'digamma' : u'\u03dd',
        'Alpha' : u'\u0391',
        'Beta' : u'\u0392',
        'Gamma' : u'\u0393',
        'Delta' : u'\u0394',
        'Epsilon' : u'\u0395',
        'Zeta' : u'\u0396',
        'Eta' : u'\u0397',
        'Theta' : u'\u0398',
        'Iota' : u'\u0399',
        'Kappa' : u'\u039a',
        'Lambda' : u'\u039b',
        'Mu' : u'\u039c',
        'Nu' : u'\u039d',
        'Ksi' : u'\u039e',
        'Omicron' : u'\u039f',
        'Pi' : u'\u03a0',
        'Rho' : u'\u03a1',
        'Sigma' : u'\u03a3',
        'Tau' : u'\u03a4',
        'Upsilon' : u'\u03a5',
        'Phi' : u'\u03a6',
        'Chi' : u'\u03a7',
        'Psi' : u'\u03a8',
        'Omega' : u'\u03a9',
        'Digamma' : u'\u03dc',
        'rough_breathing' : u'\u0314',
        'smooth_breathing' : u'\u0313',
        'acute_accent' : u'\u0301',
        'grave_acecnt' : u'\u0300',
        'circumflex' : u'\u0342',
        'iota_subscript' : u'\u0345',
        'breve' : u'\u0361',
        'diaeresis' : u'\u0308',
        'colon' : u'\u0387',
        'macron' : u'\u0304',
        'combining_overline': u'\u0305',
}

beta_code = {
        'a' : 'alpha',
        'b' : 'beta',
        'g' : 'gamma',
        'd' : 'delta',
        'e' : 'epsilon',
        'z' : 'zeta',
        'h' : 'eta',
        'q' : 'theta',
        'i' : 'iota',
        'k' : 'kappa',
        'l' : 'lambda',
        'm' : 'mu',
        'n' : 'nu',
        'c' : 'ksi',
        'o' : 'omicron',
        'p' : 'pi',
        'r' : 'rho',
        's ' : 'sigma_end',
        's' : 'sigma',
        #'s  ' : 'lunate_sigma', # use unicodedata.normalize('NFKC') to change
        # a lunate_sigma to a sigma_end
        't' : 'tau',
        'u' : 'upsilon',
        'f' : 'phi',
        'x' : 'chi',
        'y' : 'psi',
        'w' : 'omega',
        'v' : 'digamma',
        'A' : 'Alpha',
        'B' : 'Beta',
        'G' : 'Gamma',
        'D' : 'Delta',
        'E' : 'Epsilon',
        'Z' : 'Zeta',
        'H' : 'Eta',
        'Q' : 'Theta',
        'I' : 'Iota',
        'K' : 'Kappa',
        'L' : 'Lambda',
        'M' : 'Mu',
        'N' : 'Nu',
        'C' : 'Ksi',
        'O' : 'Omicron',
        'P' : 'Pi',
        'R' : 'Rho',
        'S' : 'Sigma',
        'T' : 'Tau',
        'U' : 'Upsilon',
        'F' : 'Phi',
        'X' : 'Chi',
        'Y' : 'Psi',
        'W' : 'Omega',
        'V' : 'Digamma',
        '(' : 'rough_breathing',
        ')' : 'smooth_breathing',
        '/' : 'acute_accent',
        '\\' : 'grave_acecnt',
        '=' : 'circumflex',
        '|' : 'iota_subscript',
        '\'' : 'breve',
        '+' : 'diaeresis',
        ':' : 'colon',
        '_' : 'macron',
        '~' : 'combining_overline', # not really betacode!
}

from remove_html_tags import get_html_sequences
html_sequences = get_html_sequences()

def convert_line(line):
    import unicodedata
    uppercase = False
    result = u''
    # remove odd characters - this could be handled better, but for my current
    # purposes this should be ok
    for sequence in html_sequences:
        line = line.replace(sequence, ' ')
    for i, char in enumerate(line[:-1]):
        if char in '[]!?"%#0123456789\t':
            continue
        if char == '*':
            uppercase = True
            continue
        if uppercase and char not in '()':
            char = char.upper()
            uppercase = False
        if char == 's' and line[i+1] in ' ,.:;':
            char = 's '
        if char in ' ,.-\n;\'':
            result += char
        else:
            result += greek_letters[beta_code[char]]
    result = unicodedata.normalize('NFC', result)
    return result

def main():
    import sys
    import unicodedata
    filename = sys.argv[1]
    f = open(filename)
    for line in f:
        result = convert_line(line)


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
