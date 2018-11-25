"""This script assumes the configured environment has youtube-dl and fpdf
   installed.
   Run the script from the commandline, passing in the youtube link you desire
   and the language caption that you want"""

import subprocess
import logging
import os
import argparse

#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-ytl', "--youtube_link", type=str, required=True, help="link to youtube video for exercise")
parser.add_argument("--language_initials", type=str, required=False, default="it", help="desired language, in initials. e.g. it, en, fr")
parser.add_argument("--skip", type=int, required=False, default=4, help="integer n such that every nth word is left blank")
args = parser.parse_args()
skip=args.skip
assert skip>=1
yt_link = args.youtube_link #"https://www.youtube.com/watch?v=cLuvtesdyJw"
lang_initials = args.language_initials

#download the vtt captions file
command = 'youtube-dl --write-sub --skip-download ' \
          + yt_link \
          + " --sub-lang " \
          + lang_initials \
          + " -o '%(title)s.%(ext)s'"
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if error is not None:
    print("Error obtained!")
    print(error)
    exit(1)
logging.info(output)

#open the desired (=most recent) vtt captions file
captions_pths = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith("vtt")]
captions_pths = sorted(captions_pths, key=lambda p: os.path.getmtime(p))
logging.info(captions_pths)
pth = captions_pths[0]

fh = open(pth, "r")
yt_video_title = os.path.basename(pth).split(".")[0][1:] #weird ' gets appended
captions = fh.readlines()

#remove first 4 lines, which includes metadata
captions = captions[4:]
#remove all lines which are blank (\n)
captions = [l for l in captions if l!="\n"]
#remove all timestamp lines, i.e lines including the symbol "-->"
captions = [l for l in captions if "-->" not in l]
#replace all \n in end of sentences with ""
captions = [l.replace('\n', '') for l in captions]
#combine list into one string
captions = " ".join(captions)
solutions = captions

logging.info("First 20 characters of captions")
logging.info(captions[:20])

#remove every xth word, using variable "skip"
words = captions.split(" ")
captions_blanks = []
blank="_________"
for i,w in enumerate(words, start=1): #don't want first word of captions missing
    if i % skip != 0:
        captions_blanks.append(w)
    elif not w[-1].isalpha():
        captions_blanks.append(blank + w[-1])
    else:
        captions_blanks.append(blank)

captions_blanks = " ".join(captions_blanks)

print(captions_blanks)

#create pdf
from fpdf import FPDF

pdf = FPDF() #default: Portrait, A4, millimeter unit
#pdf.set_right_margin(20)
pdf.add_page()
pdf.set_font("Arial", "B", size=14)

#video title and fill in blanks on first page
pdf.cell(w=200, h=10, txt="Fill-in-the-blanks exercise!", ln=1, align="C")
pdf.cell(w=200, h=10, txt="Watch the following video and fill in the blanks:", ln=1, align="C")

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
pdf.output("FillInBlanks.pdf")

#delete the vtt file
os.remove(pth)




