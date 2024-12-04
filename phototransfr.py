import flask, waitress, socket

app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello!</p>"
