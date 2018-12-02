#!/usr/bin/env python3

"""
This module assumes the configured environment has youtube-dl and fpdf
installed.
The module can be run as a script from the commandline, passing in the youtube
link you desire and the language caption that you want.
"""
from fpdf import FPDF
import logging
import argparse
import youtube_dl
import urllib.request
import captions as c
import os
import youtube_download as yd

def parse_args():
    '''
    @summary: Parse aguments given to the script.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-ytl', "--youtube_link", type=str, required=True,
                        help="link to youtube video for exercise")
    parser.add_argument("-l", "--language_initials", type=str, required=True,
                        help="desired language, in initials. e.g. it, en, fr")
    parser.add_argument("-s", "--skip", type=int, required=False, default=4,
                        help="integer n such that every nth word is left blank")
    parser.add_argument("-o", "--output", type=str, required=False,
                        help="path to output the PDF to.")
    parser.add_argument("-t", "--type", type=str, required=False, default="pdf",
                        choices=["pdf", "txt"], help="output file type")
    args = parser.parse_args()

    assert args.skip >= 1

    return args


def generate_output(captions, yt_video_title, output_file, output_type, skip, yt_link):
    clean_captions = c.generate_clean_solution(captions)
    captions_blanks = c.generate_caption_blanks(clean_captions, skip)

    if output_type == "pdf":
        pdf = generate_fidb_pdf(yt_video_title, yt_link, captions_blanks, clean_captions)

        if output_file is not None:
            pdf.output(output_file)
        else:
            return pdf
    elif output_type == "txt":
        out = "worksheet:\n{}\n\n\nsolutions:\n{}".format(captions_blanks,
                                                          clean_captions)
        if output_file is not None:
            with open(output_file, "w") as output_file:
                output_file.write(out)
        else:
            return out


def generate_fillindblanks(link, language_initials, n_skip, output_file=None, output_type="pdf"):
    '''
    TODO:
    '''
    ydl_wrapper = yd.YDLWrapper(link)
    yt_video_title = ydl_wrapper.get_title()
    captions = ydl_wrapper.download_captions(language_initials)
    return generate_output(captions, yt_video_title, output_file, output_type, n_skip, link)


def generate_fillindblanks_given_language(ydl_wrapper, language, n_skip, output_file=None, output_type="pdf"):
    yt_video_title = ydl_wrapper.get_title()
    language_initials = c.get_initials(language)
    captions = ydl_wrapper.download_captions(language_initials)
    link = ydl_wrapper.get_link()
    return generate_output(captions, yt_video_title, output_file, output_type, n_skip, link)


def generate_fidb_pdf(yt_video_title, yt_link, captions_blanks, solutions):
    '''
    @summary: creates exercise pdf including link to video_title, exercise, and solution
    TODO: Handle language specific fonts https://pyfpdf.readthedocs.io/en/latest/Unicode/index.html
    '''
    #create pdf
    pdf = FPDF() #default: Portrait, A4, millimeter unit
    #pdf.set_right_margin(20)
    pdf.add_page()
    pdf.add_font('DejaVu', '',
                 '{}/fonts/DejaVuSansCondensed.ttf'.format(
                     os.path.dirname(os.path.realpath(__file__))
                 ), uni=True)

    #video title and fill in blanks on first page
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(w=200, h=10,
             txt="Fill-in-the-blanks exercise!",
             ln=1, align="C")
    pdf.cell(w=200, h=10,
             txt="Watch the following video and fill in the blanks:",
             ln=1, align="C")

    pdf.set_text_color(0, 0, 255)
    pdf.cell(w=200, h=10, txt=(yt_video_title),
             link=yt_link, ln=1, align="C")
    pdf.set_text_color(0,0,0)

    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(w=0, h=10, border=1, txt=(captions_blanks))

    #solutions on second page
    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(w=200, h=10, txt="Solution:", ln=1, align="C")

    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(w=0, h=10, border=1, txt=(solutions))

    return pdf


if __name__ == '__main__':
    args = parse_args()
    skip=args.skip
    yt_link = args.youtube_link #"https://www.youtube.com/watch?v=cLuvtesdyJw"
    lang_initials = args.language_initials
    output = args.output if hasattr(args, "output") else None
    output_type = args.type
    generate_fillindblanks(yt_link, lang_initials, skip, output, output_type)

