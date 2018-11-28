#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, make_response, render_template
from fillindblanks import generate_fillindblanks
import traceback

app = Flask(__name__)

def generate_fibd_response(name, yt_link, lang_initials, skip, output_type='pdf'):
    '''
    TODO:
    @note: based on https://stackoverflow.com/questions/40149743/return-pdf-generated-with-fpdf-in-flask
    '''
    result = generate_fillindblanks(yt_link, lang_initials, skip, output_type=output_type)
    if (output_type == 'pdf'):
        pdf = result
        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers.set('Content-Type', 'application/pdf')
    elif (output_type == 'txt'):
        response = make_response(result)
    else:
        raise Exception("Unknown output type {}".format(output_type))

    response.headers.set('Content-Disposition', 'attachment', filename=name)
    return response


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/get_worksheet', methods=['POST'])
def get_worksheet():
    try:
        output_type = request.form['output_type']
        name = request.form['name'] if 'name' in request.form else 'worksheet'
        name = '.'.join([name, output_type])
        yt_link = request.form['yt_link']
        lang_initials = request.form['lang_initials']
        skip = int(request.form['skip'])
        return generate_fibd_response(name, yt_link, lang_initials, skip, output_type)
    except Exception as err:
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

