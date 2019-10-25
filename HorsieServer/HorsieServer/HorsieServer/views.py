from HorsieServer.Setup import app, request, render_template, session, flash, redirect, url_for, socketio
from flask_socketio import join_room, leave_room, emit
import HorsieServer.db as database
import datetime, random, string
from flask import jsonify

#TODO:
# If user has active session in game, and enter same with other name, close first session.

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Validate input
        if(len(request.form['Alias'])==0):
            error="Empty Alias"
        else:
            # Check existence and activity of session
            sessId = database.ActiveSessionIdFromSessionName(request.form['SessionId'])
            if(sessId == -1):
                error="No live sessions with that id"
            # Check if Alias already active in session or same sessionKey
            elif(not database.AllowUserToEnterActiveSession(sessId, request.form['Alias'], session['UserKey'] if 'UserKey' in session else "")):
                error="A user already has that Alias(Username) in that Session"
            # Enter session
            else:
                session['Alias'] = request.form['Alias']
                session['SessionId'] = sessId
                session['UserKey'] = "".join(random.choices(string.ascii_letters + string.digits,k=16))
                db = database.get_db()
                db.execute('INSERT INTO Users (SessionId, UserKey, IsActive, Alias, Standing) VALUES (?,?,?,?,?)', [sessId,session['UserKey'],1,session['Alias'],10])
                db.commit()
                return redirect(url_for('Game'))
    return render_template('index.html', error=error)

# Temp for dev
@app.route('/Game')
def Game():
    # Check Session
    if(not database.SessionActive(session['SessionId'])):
        return render_template('index.html', error="Inactive session supplied")
    # Get Users
    db = database.get_db()
    tbUsers = db.cursor().execute('SELECT * FROM Users WHERE SessionId=?',[session['SessionId']]).fetchall()
    # Get tbHorses
    tbHorses = db.cursor().execute('SELECT * FROM Horses WHERE SessionId=?',[session['SessionId']]).fetchall()   
    return render_template('Game.html', tbUsers=tbUsers, tbHorses=tbHorses)

@socketio.on('Place Bet')
def AcceptBet(json):
    print('Name and Horse ' + str(json))
    
@socketio.on('Join room')
def AssignToRoom(roomId):
    # Get info about horses:
    print("User joined room:{0}".format(roomId))
    join_room(str(roomId))
    emit("HorsesChanged",GetRelevantHorsesData(roomId))

@socketio.on('GetSaldo')
def GetUserSaldo(roomId):
    pass

def BroadCastHorsesChanged(roomId):
    print("Broadcasting to room:{0}".format(roomId))
    socketio.emit("HorsesChanged",GetRelevantHorsesData(roomId),room=str(roomId))

def GetRelevantHorsesData(roomId):
    return [dict(x) for x in database.get_db().cursor().execute('SELECT Name FROM Horses WHERE SessionId=?',[roomId]).fetchall()]