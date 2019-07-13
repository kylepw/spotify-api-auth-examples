''' Example of Spotify client credentials flow.

User can search artist names available in Spotify.

Basic flow:
    Get authorization -> get access token -> access endpoints with token

Note:
    Used in server-to-server authentication. Only can access endpoints
    that do not serve user data. Advantage of this flow over API requests
    without an access token is a higher rate limit.

Required environment variables:
    FLASK_APP, CLIENT_ID, CLIENT_SECRET, SECRET_KEY

More info:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow

'''

from flask import abort, Flask, redirect, render_template, request, session, url_for
import json
import logging
import os
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


# Client info
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Spotify API endpoints
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'


# Start 'er up
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/auth')
def auth():
    '''Get user authorization and set access token.'''

    # Request authorization from user
    payload = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'grant_type': 'client_credentials',
    }

    # `auth=(CLIENT_ID, SECRET)` basically wraps an 'Authorization'
    # header with value:
    # b'Basic ' + b64encode((CLIENT_ID + ':' + SECRET).encode())
    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    access_token = res_data.get('access_token')

    if not access_token or res.status_code != 200:
        app.logger.error(
            'Failed to get access token: %s, %s',
            res_data.get('error'),
            res_data.get('error_description'),
        )
        abort(400)
    else:
        session['access_token'] = access_token
        return redirect(url_for('search'))


def _query_artist(artist=None):
    '''Make request for data on `artist`.'''

    if artist is None:
        return artist

    payload = {'q': artist, 'type': 'artist', 'limit': '50'}
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    return requests.get(SEARCH_ENDPOINT, params=payload, headers=headers)


@app.route('/search', methods=['GET', 'POST'])
def search():
    '''Simple example search for an artist.'''

    if request.method == 'POST':

        artist = request.form.get('artist')

        if artist:
            res = _query_artist(artist)
            res_data = res.json()

            if res_data.get('error') or res.status_code != 200:
                app.logger.error(
                    'Failed to get results for %s: %s, %s',
                    artist,
                    res_data.get('error'),
                    res_data.get('error_description'),
                )
                abort(400)
            else:
                return json.dumps(res_data)

        else:
            app.logger.error('No artist value provided.')
            abort(400)

    else:

        return render_template('search.html')
