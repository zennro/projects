#!/usr/bin/env python
from flask import Flask, render_template
from flask.ext.basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

basic_auth = BasicAuth(app)

@app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')
app.run()
