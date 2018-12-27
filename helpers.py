import youtube_download as ydl
from captions import map_initials_to_language_word
from fillindblanks import generate_fillindblanks, generate_fillindblanks_given_language
from flask import make_response

def captions_from_yt_link(yt_link):
    YDL = ydl.YDLWrapper(yt_link)
    print("#####AVAILABLE CAPTIONS##########")
    print(YDL.list_available_captions())
    captions = map_initials_to_language_word(YDL.list_available_captions())
    # todo: uncomment when we want automatic captions
    # aut_captions = map_initials_to_language_word(YDL.list_automatic_captions())
    # aut_captions = [("(Automatic) " + t[0] , t[1]) for t in aut_captions]
    # captions.extend(aut_captions)
    return captions


def generate_fibd_response_given_language(yt_link, name, initials, skip, output_type):
    YDL = ydl.YDLWrapper(yt_link)
    result = generate_fillindblanks_given_language(YDL, initials, skip, output_type=output_type)
    if output_type == 'pdf':
        pdf = result
        pdf = pdf.output(dest='S')
        pdf = pdf.encode('latin-1')
        response = make_response(pdf)
        response.headers.set('Content-Type', 'application/pdf')
    elif output_type == 'txt':
        response = make_response(result)
    else:
        raise Exception("Unknown output type {}".format(output_type))

    response.headers.set('Content-Disposition', 'attachment', filename=name)
    return response


def generate_fibd_response(name, yt_link, lang_initials, skip, output_type='pdf'):
    '''
    TODO:
    @note: based on https://stackoverflow.com/questions/40149743/return-pdf-generated-with-fpdf-in-flask
    '''
    result = generate_fillindblanks(yt_link, lang_initials, skip, output_type=output_type)
    if output_type == 'pdf':
        pdf = result
        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers.set('Content-Type', 'application/pdf')
    elif output_type == 'txt':
        response = make_response(result)
    else:
        raise Exception("Unknown output type {}".format(output_type))

    response.headers.set('Content-Disposition', 'attachment', filename=name)
    return response