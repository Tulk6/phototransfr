import flask, waitress, socket, os
from flask_websockets import WebSockets, ws

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = flask.Flask(__name__)
sockets = WebSockets(app)

number_of_photos = len(os.listdir('static/photos/'))

current_photo_index = 0

def init_client_sync():
    ws.send(str(current_photo_index))

sockets.on_open(init_client_sync)

@app.route("/")
def hello_world():
    return flask.render_template("main.html")

@app.route("/photos/<path:name>")
def send_raw_photo(name):
    print(f"static/photos/{name}.jpg")
    return flask.send_from_directory(f"static/photos/", f"static/photos/{name}.jpg")

@sockets.on_message
def sync_clients(message):
    global current_photo_index
    if message == 'next':
        current_photo_index += 1
    elif message == 'prev':
        current_photo_index -= 1
    current_photo_index = min(max(0, current_photo_index), number_of_photos)
    print(current_photo_index)
    sockets.broadcast(str(current_photo_index))

server = pywsgi.WSGIServer(('james-lenovo', 4664), app, handler_class=WebSocketHandler)
server.serve_forever()