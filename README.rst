==================================
Spotify API Authorization Examples
==================================

This project contains examples of Spotify API's three authorization flows using Python/Flask:

- Authorization Code
- Client Credentials
- Implicit Grant

The *authorization code* and *implicit grant flow* examples show the
authorizing user's profile, token information, and a button that
refreshes the access token.

The *client credentials flow* example includes a search function that
lists artist information from Spotify.

.. image:: screenshots/search.png
	:width: 80%

For details on authorization flows, see `Spotify's Authorization Guide`__

__ https://developer.spotify.com/documentation/general/guides/authorization-guide/

Registration
------------
- `Register`__ your application with ``http://127.0.0.1:5000/callback`` as the redirect URI to obtain an application key and secret.

__ https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app

Setup
-----
- Clone the repository and step inside. ::

	$ git clone https://github.com/kylepw/spotify-api-auth-examples.git
	$ cd spotify-api-auth-examples

- Create a `virtual environment`__ (not required but **highly** recommended).

- Install required packages with `pip`__, `pipenv`__, or another package manager.

- Set the required environment variables as follows:

	`FLASK_APP`
		``app.py``
	`CLIENT_ID`
		Unique identifier obtained after registering your application.
	`CLIENT_SECRET`
		Key obtained after registering your application.
	`REDIRECT_URI`
		``http://127.0.0.1:5000/callback``
	`SECRET_KEY`
		Any randomized string for Flask session purposes. If unsure, just copy the output of this::

		$ python -c 'import os; print(os.urandom(16))'

	You can use `python-dotenv`__, `pipenv`__, `virtualenv or bash`__ to set the environment variables.

__ https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments
__ https://pip.pypa.io/en/stable/user_guide/#requirements-files
__ https://pipenv.readthedocs.io/en/latest/
__ https://preslav.me/2019/01/09/dotenv-files-python/
__ https://pipenv.readthedocs.io/en/latest/advanced/#automatic-loading-of-env
__ https://medium.com/@gitudaniel/the-environment-variables-pattern-be73e6e0e5b7

Usage
-----

1. Step into one of the three example folders and startup the server.

::

	$ cd authorization_code
	$ flask run
	 * Serving Flask app "app.py" (lazy loading)
 	 * Environment: development
 	 * Debug mode: on
 	 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	 ...

2. Open the address listed in a browser.

3. Click the `Login with Spotify` button and authorize the application.

License
-------
`MIT License <https://github.com/kylepw/wikiwall/blob/master/LICENSE>`_
