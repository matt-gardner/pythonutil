#!/usr/bin/env python

from optparse import OptionParser
from subprocess import Popen

LINES_PER_PAGE = 43

def make_pdf(text, width, init_path=''):
    filename = init_path + 'temp_tex_file.tex'
    file = open(filename, 'w')
    make_tex_file(file, text, width)
    file.close()
    proc = Popen(['pdflatex', filename], cwd=init_path)
    proc.wait()
    return filename[:-4] + '.pdf'


def make_tex_file(outfile, text, width=None):
    width = width or 3.0
    make_tex_preamble(outfile, width)
    make_text_header(outfile)
    make_text_data(outfile, text)
    end_text(outfile)
    finish_tex_file(outfile)


def make_tex_preamble(file, width):
    left_margin = (8 - width) / 2
    file.write('\documentclass[onecolumn, 12pt]{article}\n')
    file.write('\usepackage{fullpage}\n')
    file.write('\usepackage{framed}\n')
    file.write('\usepackage[usenames,dvipsnames]{color}\n')
    file.write('\pagestyle{empty}\n')
    file.write('\setlength{\\textwidth}{%.2fin}\n' % width)
    file.write('\setlength{\oddsidemargin}{%.2fin}\n' % left_margin)
    file.write('\\renewenvironment{leftbar}{%\n')
    file.write('\def\FrameCommand{\\textcolor{Lavender}{\\vrule width 1pt}%\n')
    file.write('\hspace{-6pt} \hspace{-%.2fin}}%%\n' % (width / 2))
    file.write('\MakeFramed {\\advance\hsize - \width \FrameRestore} }%\n')
    file.write('{\endMakeFramed}\n\n')
    file.write('\\begin{document}\n')


def make_text_header(file):
    file.write('\\begin{leftbar}\n')


def make_text_data(file, text):
    text = text.replace('$', '\$')
    text = text.replace('&', '\&')
    file.write(text)


def end_text(file):
    file.write('\end{leftbar}\n')


def finish_tex_file(file):
    file.write('\end{document}\n')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('', '--width',
            type='float',
            dest='width',
            help='Width of the text (this needs to be a float in inches)'
            )
    parser.add_option('', '--text-file',
            dest='text_file',
            help='The file from which to get the text (should be plain text)'
            )
    options, args = parser.parse_args()
    make_pdf(open(options.text_file).read(), options.width)


# vim: et sw=4 sts=4
