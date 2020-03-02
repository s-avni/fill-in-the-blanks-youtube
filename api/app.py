#!/usr/bin/env python3
import logging
import re

from flask import Flask, request, make_response
from api.part_a import is_valid_video_id
from api.part_b import generate_worksheet

app = Flask(__name__)
app.config['SECRET_KEY'] = '239045863w09txjlfdktjew40693846elkrj634096834906'
logging.basicConfig(level=logging.DEBUG)


@app.route('/check-video-id', methods=['GET', 'POST'])
def check_video_id():
    video_id = request.json['video_id']
    logging.debug(video_id)
    print(video_id)  # todo: delete & why does this change the result??
    if len(video_id) == 0:
        return {'Error': "Input cannot be empty"}
    res = is_valid_video_id(video_id)
    if isinstance(res, str):
        return {'Error': res}
    return {'langs': res}

def generate_worksheet_response(pdf, name):
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename=name)
    return response


@app.route('/get-document', methods=['GET', 'POST'])
def get_document():
    video_id = request.json['video_id']
    n = request.json['n']
    lang = request.json['lang']
    url = request.json['url']
    logging.debug(lang, n, video_id, url)
    pdf = generate_worksheet(video_id, n, url, lang)
    return generate_worksheet_response(pdf, name="Worksheet")




