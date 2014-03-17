#!/usr/bin/env python

from functools import wraps
from flask import Flask, request, Response

def check_auth(username, password):
	"""
	This function is called to check if a username/password /
	combination is valid
	"""
	return username == 'admin' and password == 'secret'

def authenticate():
	"""
	Send a 401 response that enables basic auth
	"""
	return Response(
			'Could not verify your access level for that URL. \n'
			'You have to login with proper credentials', 401,
			{'WWW-Authentificate': 'Basic realm="Login Required"'}
			)

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

app = Flask(__name__)

@app.route('/')
def index():
	return "hello"

@app.route('/secret-page')
@requires_auth
def secret_page():
	#return reder_template('secret_page.html')
	return "You in secret page"

@app.route('/user/<username>')
def user(username):
	return 'User %s' %username


if __name__ == '__main__':
	app.run(debug=True)
