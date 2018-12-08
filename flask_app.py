#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

import traceback

import youtube_dl
from flask import Flask, request, make_response, render_template, jsonify

import youtube_download as ydl
from captions import map_initials_to_language_word
from fillindblanks import generate_fillindblanks, generate_fillindblanks_given_language
import ast

app = Flask(__name__)


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


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/caption_selection', methods=['GET', 'POST'])
def caption_selection():
    try:
        yt_link = request.form['yt_link']
        captions = captions_from_yt_link(yt_link)
        return render_template("caption_selection.html", yt_link=yt_link, captions=captions)
    except youtube_dl.utils.DownloadError as err:
        print(err)
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())
    except Exception as err:
        print(type(err))
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


@app.route('/get_available_captions', methods=['GET', 'POST'])
def get_available_captions():
    try:
        yt_link = request.form['yt_link']
        captions = captions_from_yt_link(yt_link)
        return jsonify(yt_link=yt_link, captions=captions)
    except youtube_dl.utils.DownloadError as err:
        print(err)
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())
    except Exception as err:
        print(type(err))
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


@app.route('/get_worksheet', methods=['GET', 'POST'])
def get_worksheet():
    try:
        yt_link = request.form['yt_link']
        output_type = request.form['output_type']
        name = request.form['name'] if 'name' in request.form else 'fill_in_blanks_exercise'
        name = '.'.join([name, output_type])
        language_initial_tuple = request.form['language_initial_tuple'] #note: this is a string, not a tuple
        language_initial_tuple = ast.literal_eval(language_initial_tuple)
        initials = language_initial_tuple[1]
        skip = int(request.form['skip'])
        return generate_fibd_response_given_language(yt_link, name, initials, skip, output_type)
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
