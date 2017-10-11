# Kør i localhost
from os import environ
from HorsieServer import app
from HorsieServer.Setup import socketio

def HostLocal():
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    
    #app.run(HOST, PORT)
    socketio.run(app, HOST, PORT)

if __name__ == '__main__':
    HostLocal()
