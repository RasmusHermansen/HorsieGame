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
            # sessionId
            sessionId = request.form['SessionId'].upper()
            # Check existence and activity of session
            sessId = database.ActiveSessionIdFromSessionName(sessionId)
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

# Check session information and show game screen (!!!!Should be triggered by relog instead of /Game!!!!!!!)
@app.route('/Game')
def Game():
    if(len(session['Alias'])==0):
        error="Empty Alias"
    else:
        # Check existence and activity of session
        sessId = database.ActiveSessionIdFromSessionName(session['SessionId'])
        if(sessId == -1):
            error="No live sessions with that id"
        # Check if Alias already active in session or same sessionKey
        elif(not database.AllowUserToEnterActiveSession(sessId, session['Alias'], session['UserKey'] if 'UserKey' in session else "")):
            error="A user already has that Alias(Username) in that Session"
    return render_template('Game.html')


@socketio.on('Bet')
def AcceptBet(data):
    horseId = data['horse']
    amount = data['amount']
    db = database.get_db()
    # Check Odds
    odds = db.cursor().execute('SELECT Odds FROM Horses WHERE SessionId=? AND id=?',[session['SessionId'],horseId]).fetchone()[0]
    # Get user id
    id = db.cursor().execute('SELECT id FROM Users WHERE SessionId=? AND alias=?',[session['SessionId'],session['Alias']]).fetchone()[0]
    # Check Standing
    standing = GetUserStanding(session['SessionId'],id)
    # Accept bet (!!! Set a timer for minimum time between bets? !!!)
    if standing > amount:
        # Update standing
        UpdateUserStanding(session['SessionId'], id, -amount,standing)
        # Register bet
        db = database.get_db()
        db.execute('INSERT INTO Bets (SessionId, UserId, HorseId, Odds, Amount, Handled) VALUES (?,?,?,?,?,?)', 
	                    [session['SessionId'], id, horseId,  odds, amount, False])
        db.commit()
        # Update the users saldo information
        ProvideSaldoInformation()
    pass


@socketio.on('Join room')
def AssignToRoom():
    # Get info about horses:
    join_room(str(session['SessionId']))
    emit("HorsesChanged",GetRelevantHorsesData(session['SessionId']))
    emit("OddsChanged",GetReleveantOddsData(session['SessionId']))
    ProvideSaldoInformation()

def ProvideSaldoInformation():
    emit("SaldoChanged", str(GetUserStandingByAlias(session['SessionId'],session['Alias'])))

def BroadCastOddsChanged(roomId):
    socketio.emit("HorsesChanged",GetReleveantOddsData(roomId),room=str(roomId))

def BroadCastHorsesChanged(roomId):
    socketio.emit("HorsesChanged",GetRelevantHorsesData(roomId),room=str(roomId))
    BroadCastOddsChanged(roomId)

# Move below functions into DB ?
def GetRelevantHorsesData(roomId):
    return [dict(x) for x in database.get_db().cursor().execute('SELECT id, Name FROM Horses WHERE SessionId=?',[roomId]).fetchall()]

def GetReleveantOddsData(roomId):
    return [dict(x) for x in database.get_db().cursor().execute('SELECT id, Odds FROM Horses WHERE SessionId=?',[roomId]).fetchall()]

def GetUserStandingByAlias(sessionId, alias):
    return database.get_db().cursor().execute('SELECT Standing FROM Users WHERE SessionId=? AND Alias=?',[sessionId,alias]).fetchone()[0]

def GetUserStanding(sessionId, id):
    return database.get_db().cursor().execute('SELECT Standing FROM Users WHERE SessionId=? AND id=?',[sessionId,id]).fetchone()[0]

def UpdateUserStanding(sessionId, id, change, current = None):
    db = database.get_db()
    if not current:
        current = GetUserStandingWithID(sessionId, id)
    db.cursor().execute("UPDATE Users SET Standing = ? WHERE SessionId=? AND id=?",[current + change,sessionId,id])
    db.commit()
