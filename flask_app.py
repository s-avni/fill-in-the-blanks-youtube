#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

import traceback

import youtube_dl
from flask import Flask, request, make_response, render_template, jsonify
import werkzeug

import youtube_download as ydl
from captions import map_initials_to_language_word
from fillindblanks import generate_fillindblanks, generate_fillindblanks_given_language
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

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
    return render_template('index.html')


@app.route('/caption_selection', methods=['GET', 'POST'])
def caption_selection():
    response = render_template(
        'homepage.html', errorMsg="An unexpected error occured")
    try:
        assert 'yt_link' in request.form, "Could not get Youtube URL from form."
        yt_link = request.form['yt_link']
        assert yt_link != '', "You did not pass a URL"
        captions = captions_from_yt_link(yt_link)
        response = render_template("caption_selection.html", yt_link=yt_link, captions=captions)
    except youtube_dl.utils.DownloadError as err:
        print(type(err), str(err), traceback.format_exc())
        response = render_template('homepage.html', errorMsg="Youtube download error - check the URL you provided")
    except AssertionError as err:
        print(type(err), str(err), traceback.format_exc())
        if str(err):
            response = render_template('homepage.html', errorMsg=(str(err)))
    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
    return response

@app.route('/get_available_captions', methods=['GET', 'POST'])
def get_available_captions():
    yt_link = None
    try:
        req_data = request.get_json()
        yt_link = req_data['yt_link']
        captions = captions_from_yt_link(yt_link)
        return jsonify(yt_link=yt_link, captions=captions)
    except youtube_dl.utils.DownloadError as err:
        print(type(err), str(err), traceback.format_exc())
        return jsonify(error="Youtube download error - check the URL you provided")
    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
        if (yt_link is not None):
            return jsonify(error="An error occured while trying to get captions for `{}`".format(yt_link))
        else:
            return jsonify(error="Failed to recieve youtube link in request")


@app.route('/get_worksheet', methods=['GET', 'POST'])
def get_worksheet():
    response = render_template(
        'homepage.html', errorMsg="An unexpected error occured")

    try:
        yt_link = request.form['yt_link']
        output_type = request.form['output_type']
        name = request.form['name'] if 'name' in request.form else 'fill_in_blanks_exercise'
        name = '.'.join([name, output_type])
        lang_initials = request.form['lang_initials']
        skip = int(request.form['skip'])
        return generate_fibd_response_given_language(yt_link, name, lang_initials, skip, output_type)
    except youtube_dl.utils.DownloadError as err:
        print(type(err), str(err), traceback.format_exc())
        response = render_template(
            'homepage.html', errorMsg="A Youtube download error occured")

    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
    return response


@app.route('/fidb_worksheet_test')
def test_worksheet():
    '''
    TODO:
    '''
    response = render_template(
        'homepage.html', errorMsg="An unexpected error occured")
    try:
        name = 'Harry_Potter_Fill_In_Blanks.pdf'
        yt_link = 'https://www.youtube.com/watch?v=y57sYHIDP_Y&t=6s'
        lang_initials = 'en'
        skip = 4
        response = generate_fibd_response(name, yt_link, lang_initials, skip)
    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
    return response

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print("Bad request", request, e)
    return 'bad request!', 400

if __name__ == "__main__":
    app.run(debug=True)

# todo: handle input errors gracefully!
