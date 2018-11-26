#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, make_response
from fillindblanks import generate_fillindblanks
import traceback

app = Flask(__name__)

def generate_fibd_response(name, yt_link, lang_initials, skip):
    '''
    TODO:
    '''
    pdf = generate_fillindblanks(yt_link, lang_initials, skip)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename=name)
    response.headers.set('Content-Type', 'application/pdf')
    return response


@app.route('/')
def hello_world():
    return "<a href='/fidb_worksheet_test'>Try our our demo worksheet!</a>"

@app.route('/fidb_worksheet_test')
def test_worksheet():
    '''
    TODO:
    '''
    try:
        name = 'test.pdf'
        yt_link = 'https://www.youtube.com/watch?v=3a7SLcK2_h4'
        lang_initials = 'en'
        skip = 5
        return generate_fibd_response(name, yt_link, lang_initials, skip)
    except Exception as err:
        return "An error occured: {}\nTraceback:\n{}".format(str(err), traceback.format_exc())


# TODO: https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
# TODO: for cleanupt: http://flask.pocoo.org/docs/1.0/api/#flask.after_this_request
