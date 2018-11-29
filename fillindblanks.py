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
import os

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


def youtube_download_subs(yt_link, lang_initials):
    try:
        ydl_opts = {"skip_download" : True,
                    "writesubtitles" : True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=False)
            title = info['title']
            subtitle_dict = info["subtitles"]
            #get the plain link of subtitles
            desired_subtitles_link = subtitle_dict[lang_initials][1]['url']
            print(desired_subtitles_link)

            tmp_file, _ = urllib.request.urlretrieve(desired_subtitles_link)
            with open(tmp_file) as f:
                content = f.read()

            # content = content.decode("utf-8") #decode to utf-8 (originally in bytes)
            content = content.splitlines()
    finally:
        urllib.request.urlcleanup()

    return title, content


def generate_fillindblanks(yt_link, lang_initials, skip, output_file=None, output_type="pdf"):
    '''
    TODO:
    '''
    yt_video_title, captions = youtube_download_subs(yt_link, lang_initials)

    clean_captions = generate_clean_solution(captions)
    captions_blanks = generate_caption_blanks(clean_captions, skip)
    print(captions_blanks[:50]) #todo: assumes length is > 50...change to logging and check

    if (output_type == "pdf"):
        pdf = generate_fidb_pdf(yt_video_title, yt_link, captions_blanks, clean_captions)

        if output_file is not None:
            pdf.output(output_file)
        else:
            return pdf
    elif (output_type == "txt"):
        output = "worksheet:\n{}\n\n\nsolutions:\n{}".format(captions_blanks,
                                                           clean_captions)
        if output_file is not None:
            with open(output_file, "w") as output_file:
                output_file.write(output)
        else:
            return output

def generate_clean_solution(captions):
    '''
    @summary: returns clean solution string from captions vtt file
    :param captions:
    :return:
    '''
    # remove first 4 lines, which includes metadata
    captions = captions[4:]
    # remove all timestamp lines, i.e lines including the symbol "-->"
    captions = [l for l in captions if "-->" not in l]
    # replace all \n in end of sentences with ""
    captions = [l.replace('\n', '') for l in captions]
    # remove all lines which are blank
    captions = [l for l in captions if len(l) > 0]
    # combine list into one string
    captions = " ".join(captions)

    logging.info("First 20 characters of captions")
    logging.info(captions[:20])

    return captions


def generate_caption_blanks(captions, skip):
    '''
    @summary: creates exercise string with blanks from the solution string
    '''
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

    return " ".join(captions_blanks)



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

