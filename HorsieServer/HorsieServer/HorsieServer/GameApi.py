from flask_socketio import send, emit
from flask import jsonify
from HorsieServer.Setup import socketio
import HorsieServer.db as database
import datetime, random, string

gameSessions = []

