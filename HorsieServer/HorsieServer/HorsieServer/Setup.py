import os, datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_socketio import SocketIO
## INIT APP ##

app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(
    #DEBUG= True,
    DATABASE= os.path.join(app.root_path, 'Horsie.db'),
    SECRET_KEY= 'fTcCO24fOIcMShAvHJ5v7TVEuEnKoaQPMLvX5PRw'
    ))

socketio = SocketIO(app)
'''
@app.before_first_request
def PersistentSession():
    session.permanent = True;
    app.permanent_session_lifetime = datetime.timedelta(minutes=30)
'''

import HorsieServer.db as db
import HorsieServer.views
import HorsieServer.WebApi
import HorsieServer.GameApi