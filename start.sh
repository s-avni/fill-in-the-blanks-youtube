#!/bin/bash
export FLASK_ENV=development
export FLASK_APP=./api/app.py
flask run --no-debugger #no-debugger b/c flask is only used as an api, not to serve webpages
#see https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
