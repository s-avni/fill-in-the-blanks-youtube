#!/usr/bin/env python3

# A very simple Flask Hello World app for you to get started with...

import traceback

import werkzeug
import youtube_dl
from flask import Flask, request, render_template, url_for, session, redirect, flash

from forms import YTLinkForm, WorksheetForm
from helpers import captions_from_yt_link, generate_fibd_response_given_language, generate_fibd_response

app = Flask(__name__)
app.config['SECRET_KEY'] = '239045863w09txjlfdktjew40693846elkrj634096834906'
# app.config.update(
#     RECAPTCHA_ENABLED = True,
#     RECAPTCHA_PUBLIC_KEY = 'mypublickey',
#     RECPATCHA_PRIVATE_KEY = 'myprivatekey',
# )


#todo: make templates suitable for phones (see Bootstrap columns info online)


#todo: forms are definitely an overkill here. because the homepage is such a simple form and we are using
#todo: form objects, then we have to create these objects for each redirect to the homepage
#todo: either see how we avoid this, or get rid of form objects, although it was fun implementing them!

#todo: we are encountering some version of the get-post problem, where when we go back in the browser
#todo: we are asked if we want to resubmit the form. we should deal with this gracefully

#todo: i have used sessions, but that is probably overkill as well. to google: pros/cons of sessions

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(str(error))

@app.route('/', methods=['GET', 'POST'])
def index():
    link = None
    form = YTLinkForm()
    if form.validate_on_submit():
        link = form.link.data
        session['link'] = link
        return redirect(url_for('caption_selection'))
    elif form.errors is not None:
        flash_errors(form)
        print(form.errors)
    return render_template('index.html', form=form, link=link)


@app.route('/caption_selection', methods=['GET', 'POST'])
def caption_selection():
    link = session['link']
    form = WorksheetForm()
    index_form = YTLinkForm()
    try:
        captions = captions_from_yt_link(link.strip())
        print("!!")
        print(captions)
        form.caption_lang.choices = captions  # dynamic choices
    except youtube_dl.utils.DownloadError as err:
        print(type(err), str(err), traceback.format_exc())
        flash("Youtube download error - check the URL you provided")
        response = render_template("index.html", form=index_form)
        return response
    except Exception as err:
        flash(str(err))
        print(type(err), str(err), traceback.format_exc())
        flash("An error occurred. Please email the site admins if this happens again.")
        response = render_template("index.html", form=index_form)
        return response
    if form.validate_on_submit():
        session['output_type'] = form.output_type.data
        session['name'] = form.file_name.data
        session['skip'] = int(form.skip_every.data)
        for lang, initials in captions:  # todo: yucky
            if lang == form.caption_lang.data:
                session['lang_initials'] = initials
        print(session['lang_initials'])
        return redirect(url_for('get_worksheet'))
    elif form.errors is not None:
        flash_errors(form)
        print(form.errors)
    return render_template('page2.html', form=form, yt_link=link)


@app.route('/get_worksheet', methods=['GET'])
def get_worksheet():
    index_form = YTLinkForm()  # todo: yuck, to take care of
    try:
        name = '.'.join([session['name'], session['output_type']])
        return generate_fibd_response_given_language(session['link'],
                                                     name,
                                                     session['lang_initials'],
                                                     session['skip'],
                                                     session['output_type'])
    except youtube_dl.utils.DownloadError as err:
        print(type(err), str(err), traceback.format_exc())
        response = render_template("index.html", form=index_form)
        flash("A Youtube download error occured")
    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
        response = render_template("index.html", form=index_form)
        flash("An unexpected error occured")
    return response


# @app.route('/get_available_captions', methods=['GET', 'POST'])
# def get_available_captions():
#     yt_link = None
#     try:
#         req_data = request.get_json()
#         yt_link = req_data['yt_link']
#         captions = captions_from_yt_link(yt_link)
#         return jsonify(yt_link=yt_link, captions=captions)
#     except youtube_dl.utils.DownloadError as err:
#         print(type(err), str(err), traceback.format_exc())
#         return jsonify(error="Youtube download error - check the URL you provided")
#     except Exception as err:
#         print(type(err), str(err), traceback.format_exc())
#         if (yt_link is not None):
#             return jsonify(error="An error occured while trying to get captions for `{}`".format(yt_link))
#         else:
#             return jsonify(error="Failed to recieve youtube link in request")

@app.route('/fidb_worksheet_test')
def test_worksheet():
    '''
    TODO:
    '''
    try:
        name = 'Harry_Potter_Fill_In_Blanks.pdf'
        yt_link = 'https://www.youtube.com/watch?v=y57sYHIDP_Y&t=6s'
        lang_initials = 'en'
        skip = 4
        response = generate_fibd_response(name, yt_link, lang_initials, skip)
    except Exception as err:
        print(type(err), str(err), traceback.format_exc())
        flash("An unexpected error occured")
        index_form = YTLinkForm()  # todo: yuck, to take care of
        response = render_template("index.html", form=index_form)
    return response


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print("Bad request", request, e)
    return 'bad request!', 400


if __name__ == "__main__":
    app.run(debug=True)

# todo: handle input errors gracefully!
