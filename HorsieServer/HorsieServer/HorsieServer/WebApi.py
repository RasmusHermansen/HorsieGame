from HorsieServer.Setup import app, request, abort
import HorsieServer.db as database
import datetime, random, string
from flask import jsonify

# TODO:
# REMOVE GET from methods for entire api

@app.route('/Game/api/v1.0/CreateSession', methods=['GET','POST'])
def CreateSession():
    #replace sessionNames with valid generator
    sessionNames = ("Memes", "Krugge", "BaNAn", "wololo", "brikken", "kony")
    
    sessionName = ""
    # Iterate new SessionNames untill valid
    counter = 0;
    while True:
        # Create SessionName
        sessionName = random.choice(sessionNames)
        # Check if it is unique and inactive
        sessId = database.ActiveSessionIdFromSessionName(sessionName)
        if(sessId == -1):
            break
        # SessionName iterations
        counter += 1
        # Cleanup activeSessions
        if(counter > 25):
            raise RecursionError("Unable to create new unique active session, check if IsActive for all sessNames")

    # Generate key
    sessionKey = "".join(random.choices(string.ascii_letters + string.digits,k=16))

    # Create Session
    db = database.get_db()
    db.execute('INSERT INTO Sessions (SessionName, SessionKey, IsActive, Created) VALUES (?,?,1,?)', 
	                    [sessionName,sessionKey,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    db.commit()
    # Get new sessionId
    return jsonify({'sessionName': sessionName, 'uniqueId': database.ActiveSessionIdFromSessionName(sessionName), 'sessionKey':sessionKey})

def _ValidRequest(request):
    """ Ensures request is Json, session is active and the correct session key is supplied"""
    if not request.json:
        abort(400)
    sessId = request.json['sessionId']
    sessKey = request.json['sessionKey']
    # Check if it is active and correct key
    return database.SessionActive(sessId) and database.CorrectSessionKey(sessId, sessKey)

@app.route('/Game/api/v1.0/CloseSession', methods=['GET','POST'])
def CloseSession():
    if(_ValidRequest(request)):
        # Close Session
        db = database.get_db()
        db.execute('UPDATE Sessions SET IsActive = 0, Closed = ? WHERE id=?', 
	                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),sessId])
        db.commit()

    return jsonify({'Closed': True})

@app.route('/Game/api/v1.0/SetHorses', methods=['GET','POST'])
def SetHorses():
    if(_ValidRequest(request)):
        desiredHorses = request.json['horsesCount']
        # Init db
        db = database.get_db()
        # Get count of horses
        numberHorses = db.cursor().execute('SELECT COUNT(*) FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchone()[0]
        # add or remove horses
        if(numberHorses > desiredHorses):
            db.execute('DELETE FROM Horses WHERE id IN (SELECT id FROM Horses WHERE SessionId=? LIMIT ?)',[request.json['sessionId'],numberHorses-desiredHorses])
            db.commit()
        elif(numberHorses < desiredHorses):
            horseNames = ("Tarok", "Tarok1", "TArok2", "Mustafa", "Donkey", "1949", "DenSorteDød", "HvorDuFra")
            for i in range(0,desiredHorses - numberHorses):
                db.execute('INSERT INTO Horses (SessionId, Name, Speed) VALUES (?,?,?)', 
	                            [request.json['sessionId'],random.choice(horseNames),random.randint(0,10)])
                db.commit()
        # Get horses
        tbl_Horses = db.cursor().execute('SELECT Name, Speed FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchall()
        
        return jsonify({'Horses':[dict(x) for x in tbl_Horses]})

@app.route('/Game/api/v1.0/GetAllBets', methods=['GET','POST'])
def GetAllBets():
    raise NotImplementedError()
    if not request.json:
        abort(400)
    sessId = request.json['sessionId']
    sessKey = request.json['sessionKey']
    sessRun = request.json['sessionRun']
    # Check if it is active and correct key
    if(not database.SessionActive(sessId) or not database.CorrectSessionKey(sessId, sessKey)):
        raise ConnectionRefusedError("Inactive sessionId or invalid sessionKey")
    # Make query
    db = database.get_db()
    bets = db.cursor().execute('SELECT ActionId FROM Actions WHERE SessionId=?',[session['SessionId']]).fetchall()

    return jsonify({'Closed': True})