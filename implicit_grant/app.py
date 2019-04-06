''' Example of Spotify implicit grant flow.

Basic flow:
    -> Request authorization
    -> Get access token through fragment identifier
    -> Access API endpoints with token

Notes:
    This flow can be implemented client-side in JS because
    because no secret keys are used. No refresh token
    is provided.

    This example uses Python/Flask, but it is probably better
    to go 100% client-side. The access token is supplied as part
    of a URI fragment identifier, which the server-side cannot see,
    so confirming `state` (ensuring that the response/request came
    from the same browser) with cookies, etc. would be difficult
    (impossible?).

Required environment variables:
    FLASK_APP, CLIENT_ID

More info:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow

'''

from flask import abort, Flask, make_response, redirect, render_template, request
import logging
import os
import secrets
import string
from urllib.parse import urlencode


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


# Client info
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'


# Start 'er up
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/auth')
def auth():

    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    # Request authorization from user
    # Only including `state` here for error logging purposes.
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'token',
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-read-private user-read-email',
        'state': state,
    }

    res = make_response(redirect(f'{AUTH_URL}/?{urlencode(payload)}'))

    return res


@app.route('/callback')
def callback():
    error = request.args.get('error')
    state = request.args.get('state')

    if error:
        app.logger.error('Error: %s, State: %s', error, state)
        abort(400)

    return render_template('profile.html')
