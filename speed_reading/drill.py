#!/usr/bin/env python

from optparse import OptionParser
from random import randint

LINES_PER_PAGE = 43

def main(options):
    f = open('temporary_tex_file.tex', 'w')
    make_tex_preamble(f)
    num_letter_cols = options.num_letter_cols or 3
    num_center_letters = options.num_center_letters or 1
    num_lines = options.lines_at_a_time or 0
    width = options.width or '1.5in'
    make_table_header(f, num_letter_cols, num_center_letters, width)
    make_table_data(f, num_letter_cols, num_center_letters, num_lines)
    end_table(f)
    finish_tex_file(f)
    f.close()


def make_tex_preamble(file):
    file.write('\documentclass[onecolumn, 12pt]{article}\n')
    file.write('\usepackage{fullpage}\n')
    file.write('\usepackage{multicol}\n')
    file.write('\setlength{\parindent}{0in}\n\n')
    file.write('\\begin{document}\n')


def make_table_header(file, num_letter_cols, num_center_letters, width):
    file.write('\\begin{center}')
    file.write('\\begin{tabular*}{')
    file.write(width)
    file.write('}{')
    for i in range(num_letter_cols - 1):
        file.write('c @{\extracolsep{\\fill}} ')
    file.write('c}\n')


def make_table_data(file, num_letter_cols, num_center_letters, num_lines=0):
    for l in range(LINES_PER_PAGE):
        bold = num_lines != 0 and (l - 1) % num_lines == 0
        for c in range(num_letter_cols - 1):
            if c == int(num_letter_cols) / 2:
                num_letters = num_center_letters
                center = True
            else:
                num_letters = 1
                center = False
            for r in range(num_letters):
                if bold and center and r == int(num_letters) / 2:
                    file.write(highlight(random_char()))
                else:
                    file.write(random_char())
            file.write('&')
        file.write(random_char())
        file.write('\\\\\n')

def random_char():
    return chr(randint(0,25) + ord('A'))


def highlight(char):
    return '\underline{\\textbf{' + char + '}}'


def end_table(file):
    file.write('\end{tabular*}\n')
    file.write('\end{center}\n')


def finish_tex_file(file):
    file.write('\end{document}\n')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('', '--num-letter-cols',
            type='int',
            dest='num_letter_cols',
            help='Number of columns of letters (should be odd)'
            )
    parser.add_option('', '--num-center-letters',
            type='int',
            dest='num_center_letters',
            help='Number of letters in the center column (should be odd)'
            )
    parser.add_option('', '--width',
            dest='width',
            help='Width of the columns (this needs to be a LaTeX width '
            'specification'
            )
    parser.add_option('', '--lines-at-a-time',
            type='int',
            dest='lines_at_a_time',
            help='Number of lines to drill at a time (center letter will be '
            'bolded)'
            )
    options, args = parser.parse_args()
    main(options)


# vim: et sw=4 sts=4
