"""frontend langing page"""
import flask
import get_a_wai


@get_a_wai.app.route('/', methods=['GET'])
def index():
    return flask.render_template("index.html",)

# @get_a_wai.app.route('/js/<path:filename>')
# def download_react():
#     return flask.send_from_directory(get_a_wai.app.config90)

