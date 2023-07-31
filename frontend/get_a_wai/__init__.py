
"""frontend package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module
app.config.from_object('get_a_wai.config')

import get_a_wai.views  # noqa: E402  pylint: disable=wrong-import-position
