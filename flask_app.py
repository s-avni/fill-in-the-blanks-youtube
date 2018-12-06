#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, make_response, render_template, redirect, url_for
from fillindblanks import generate_fillindblanks, generate_fillindblanks_given_language
import youtube_download as ydl
from captions import map_initials_to_language_word
import traceback
import youtube_dl

app = Flask(__name__)
YDL = None


def generate_fibd_response_given_language(name, language, skip, output_type):
    result = generate_fillindblanks_given_language(YDL, language, skip, output_type=output_type)
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


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/get_available_captions', methods=['GET','POST'])
def get_available_captions():
    global YDL
    try:
        yt_link = request.form['yt_link']
        YDL = ydl.YDLWrapper(yt_link)
        print("###############")
        print(YDL.list_available_captions())
        captions = map_initials_to_language_word(YDL.list_available_captions())
        aut_captions = map_initials_to_language_word(YDL.list_automatic_captions())
        aut_captions = ["(Automatic) " + c for c in aut_captions]
        captions.extend(aut_captions)
        return render_template("caption_selection.html", captions=captions)
    except youtube_dl.utils.DownloadError as err:
        print(err)
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())
    except Exception as err:
        print(type(err))
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


@app.route('/get_worksheet', methods=['GET','POST'])
def get_worksheet():
    try:
        output_type = request.form['output_type']
        name = request.form['name'] if 'name' in request.form else 'fill_in_blanks_exercise'
        name = '.'.join([name, output_type])
        language = request.form['language']
        skip = int(request.form['skip'])
        return generate_fibd_response_given_language(name, language, skip, output_type)
    except youtube_dl.utils.DownloadError as err:
        print(err)
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())
    except Exception as err:
        print(type(err))
        print(err)
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


@app.route('/fidb_worksheet_test')
def test_worksheet():
    '''
    TODO:
    '''
    try:
        name = 'test.pdf'
        yt_link = 'https://www.youtube.com/watch?v=mDclQowcE9I'
        lang_initials = 'en'
        skip = 5
        return generate_fibd_response(name, yt_link, lang_initials, skip)
    except Exception as err:
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


if __name__ == "__main__":
    app.run(debug=True)

# todo: handle input errors gracefully!
