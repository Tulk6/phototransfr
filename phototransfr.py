import flask, waitress, socket, os, json
from flask_websockets import WebSockets, ws
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

with open('photo_manifest.txt') as f:
    photo_manifest = json.loads(f.read())

app = flask.Flask(__name__)
sockets = WebSockets(app)

number_of_photos = len(os.listdir('static/photos/'))

current_photo_index = 0

def get_image_info(photo_index):
    img_date = photo_manifest[str(photo_index)]['datetime']
    img_caption = photo_manifest[str(photo_index)]['caption']
    img_index = str(photo_index)
    return f'{img_index}|{img_date}|{img_caption}'

def init_client_sync():
    ws.send(get_image_info(current_photo_index))

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
    else:
        current_photo_index = int(message)
    current_photo_index = min(max(0, current_photo_index), number_of_photos-1)
    print(current_photo_index)
    sockets.broadcast(get_image_info(current_photo_index))

server = pywsgi.WSGIServer((socket.gethostname(), 4664), app, handler_class=WebSocketHandler)
server.serve_forever()

