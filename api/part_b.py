import logging
from youtube_transcript_api import YouTubeTranscriptApi
import re
from fpdf import FPDF
import os

def generate_pdf(text, text_with_blanks, url):
    pdf = FPDF()  # default: Portrait, A4, millimeter unit
    pdf.compress = 0
    pdf.add_page()
    pre_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    pdf.add_font('DejaVu', '',
                 '{}/fonts/DejaVuSansCondensed.ttf'.format(pre_path), uni=True)

    # video title and fill in blanks on first page
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(w=200, h=10,
             txt="Fill-in-the-blanks exercise!",
             ln=1, align="C")
    pdf.cell(w=200, h=10,
             txt="Watch the following video and fill in the blanks:",
             ln=1, align="C")

    # important!! keep dejavu font so that title can be outputted correctly!
    # dejavu has no bold style
    pdf.set_font("DejaVu", size=14)

    pdf.set_text_color(0, 0, 255)

    pdf.cell(w=200, h=10, txt=url,
             link=url, ln=1, align="C")

    pdf.set_text_color(0, 0, 0)

    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(w=0, h=10, border=1, txt=text_with_blanks, align="L")

    # solutions on second page
    pdf.add_page()
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(w=200, h=10, txt="Solution:", ln=1, align="C")

    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(w=0, h=10, border=1, txt=text, align="L")

    return pdf


def generate_worksheet(video_id, n, url, lang):
    text = get_clean_text(video_id, lang)
    text_with_blanks = generate_caption_blanks(text, skip=n)
    pdf = generate_pdf(text, text_with_blanks, url)
    return pdf


def get_clean_text(video_id, lang):
    transcript_list = YouTubeTranscriptApi.get_transcripts([video_id], languages=[lang])
    transcript = transcript_list[0][video_id]
    text = [elem['text'] for elem in transcript]
    clean_text = [elem.replace("\n", " ") for elem in text]
    clean_text = " ".join(clean_text)
    # remove text in square brackets, as this describes the video but is not heard. e.g [theme music]
    # assumes no nested brackets, which is true for youtube videos
    clean_text = re.sub("[\[].*?[\]]", "", clean_text)
    logging.info("First 20 characters of captions")
    logging.info(clean_text[:20])
    return clean_text


def generate_caption_blanks(captions, skip):
    '''
    @summary: creates exercise string with blanks from the solution string
    '''
    # remove every xth word, using variable "skip"
    words = captions.split(" ")
    # remove all empty words
    words = [w for w in words if len(w) > 0]
    captions_blanks = []
    blank = "_________"
    for i, w in enumerate(words, start=1):  # don't want first word of captions missing
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

url = "https://www.youtube.com/watch?v=MKlx1DLa9EA"
pdf = generate_worksheet("MKlx1DLa9EA", 3, url,'en')
pdf.output(name = '/home/shiri/Desktop/worksheet.pdf', dest = 'F')
