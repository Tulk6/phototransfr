import flask, waitress, socket
from flask_websockets import WebSockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = flask.Flask(__name__)
sockets = WebSockets(app)

@app.route("/")
def hello_world():
    return flask.render_template("main.html")

@app.route("/photos/<path:name>")
def send_raw_photo(name):
    print(name)
    root_dir, photo_index = name.split('_')
    print(root_dir, photo_index)
    print(f"static/photos/{root_dir}/DSCF{photo_index}.jpg")
    return flask.send_from_directory(f"static/photos/", f"{root_dir}/DSCF0{photo_index}.jpg")

@sockets.on_message
def echo(message):
    return message

server = pywsgi.WSGIServer(('james-lenovo', 4664), app, handler_class=WebSocketHandler)
server.serve_forever()