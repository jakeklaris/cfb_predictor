"""
CFB_PREDICTOR (main) view

URLs include:
/
"""
import flask
import cfb_predictor

@cfb_predictor.app.route('/')
def show_index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)