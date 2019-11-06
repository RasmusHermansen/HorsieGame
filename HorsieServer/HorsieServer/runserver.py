from os import environ
from HorsieServer import app
from HorsieServer.db import init_db
from HorsieServer.Setup import socketio

def HostLocal():
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run(app, HOST, PORT)

def HostLocalOpen():
    # Fixed Port for shizzle
    socketio.run(app, '0.0.0.0', '5555')

if __name__ == '__main__':
    HostLocalOpen()
