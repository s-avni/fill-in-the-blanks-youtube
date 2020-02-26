#!/usr/bin/env python3
import traceback
import werkzeug
import youtube_dl
from flask import Flask, request, render_template, url_for, session, redirect, flash, send_from_directory

from forms import YTLinkForm, WorksheetForm
from helpers import captions_from_yt_link, generate_fibd_response_given_language, generate_fibd_response

app = Flask(__name__)
app.config['SECRET_KEY'] = '239045863w09txjlfdktjew40693846elkrj634096834906'

@app.route('/analyse-youtube-link')
def analyse-youtube-link():
    return {'time': time.time()}


