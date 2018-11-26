#!/usr/bin/env python3

"""
This module assumes the configured environment has youtube-dl and fpdf
installed.
The module can be run as a script from the commandline, passing in the youtube
link you desire and the language caption that you want.
"""
from fpdf import FPDF
import subprocess
import logging
import os
import argparse
import traceback

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
    args = parser.parse_args()

    assert args.skip >= 1

    return args


def youtube_download_subs(yt_link, lang_initials):
    #download the vtt captions file
    command = 'youtube-dl --write-sub --skip-download ' \
              + yt_link \
              + " --sub-lang " \
              + lang_initials \
              + " -o '%(title)s.%(ext)s'"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error is not None:
        print("Error occured!")
        print(error)
        traceback.print_exc()
        raise Exception(error)

    logging.info(output)
    return output


def generate_fillindblanks(yt_link, lang_initials, skip, output_file=None):
    '''
    TODO:
    '''
    captions_pths = []
    try:
        # TODO: upgrade to using import - https://github.com/rg3/youtube-dl/blob/master/README.md#readme
        output = youtube_download_subs(yt_link, lang_initials)

        # open the desired (=most recent) vtt captions file
        captions_pths = [f for f in os.listdir('.')
                         if os.path.isfile(f) and f.endswith("vtt")]
        captions_pths = sorted(captions_pths, key=lambda p: os.path.getmtime(p))
        logging.info(captions_pths)
        pth = captions_pths[0]

        yt_video_title = os.path.basename(pth).split(".")[0][1:] #weird ' gets appended

        with open(pth, "r") as fh:
            captions = fh.readlines()

        captions_blanks, solutions = generate_caption_blanks(captions)
        print(captions_blanks)
        pdf = generate_fidb_pdf(yt_video_title, captions_blanks, solutions)

        if output_file is not None:
            pdf.output(output_file)
        else:
            return pdf
    finally:
        #delete the vtt files
        for cpth in captions_pths:
            os.remove(cpth)


def generate_caption_blanks(captions):
    '''
    TODO:
    '''

    #remove first 4 lines, which includes metadata
    captions = captions[4:]
    #remove all timestamp lines, i.e lines including the symbol "-->"
    captions = [l for l in captions if "-->" not in l]
    #replace all \n in end of sentences with ""
    captions = [l.replace('\n', '') for l in captions]
    #remove all lines which are blank
    captions = [l for l in captions if len(l) > 0]
    #combine list into one string
    captions = " ".join(captions)
    solutions = captions

    logging.info("First 20 characters of captions")
    logging.info(captions[:20])

    #remove every xth word, using variable "skip"
    words = captions.split(" ")
    #remove all empty words
    words = [w for w in words if len(w) > 0]
    captions_blanks = []
    blank="_________"
    for i,w in enumerate(words, start=1): #don't want first word of captions missing
        try:
            if i % skip != 0:
                captions_blanks.append(w)
            elif not w[-1].isalpha():
                # Keep punctuations at the end of words
                captions_blanks.append(blank + w[-1])
            else:
                captions_blanks.append(blank)
        except:
            logging.error("Failed on word {}/{}: '{}'".format(i, len(words), w))
            raise

    return " ".join(captions_blanks), solutions



def generate_fidb_pdf(yt_video_title, captions_blanks, solutions):
    '''
    TODO:
    '''
    #create pdf
    pdf = FPDF() #default: Portrait, A4, millimeter unit
    #pdf.set_right_margin(20)
    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)

    #video title and fill in blanks on first page
    pdf.cell(w=200, h=10,
             txt="Fill-in-the-blanks exercise!",
             ln=1, align="C")
    pdf.cell(w=200, h=10,
             txt="Watch the following video and fill in the blanks:",
             ln=1, align="C")

    pdf.set_text_color(0, 0, 255)
    pdf.cell(w=200, h=10, txt=yt_video_title,
             link=yt_link, ln=1, align="C")
    pdf.set_text_color(0,0,0)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(w=0, h=10, border=1, txt=captions_blanks)

    #solutions on second page
    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(w=200, h=10, txt="Solution:", ln=1, align="C")

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(w=0, h=10, border=1, txt=solutions)

    return pdf


if __name__ == '__main__':
    #command line arguments
    args = parse_args()
    skip=args.skip
    yt_link = args.youtube_link #"https://www.youtube.com/watch?v=cLuvtesdyJw"
    lang_initials = args.language_initials
    output = args.output if hasattr(args, "output") else None
    generate_fillindblanks(yt_link, lang_initials, skip, output)


