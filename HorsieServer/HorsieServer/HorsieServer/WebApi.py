from HorsieServer.Setup import app, request, abort, socketio
from HorsieServer.views import BroadCastHorsesChanged
from HorsieServer.HorseClasses import HorseClasses
import HorsieServer.db as database
import datetime, random, string
from scipy import interpolate
from flask import jsonify


# TODO:
# REMOVE GET from methods for entire api

@app.route('/Game/api/v1.0/CreateSession', methods=['GET','POST'])
def CreateSession():
    #replace sessionNames with valid generator
    sessionNames = ("KONY","PONY")
    
    sessionName = ""
    # Iterate new SessionNames untill valid
    counter = 0;
    while True:
        # Create SessionName
        sessionName = random.choice(sessionNames) + str(random.randint(1,100))
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
	                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),request.json['sessionId']])
        db.commit()

    return jsonify({'Closed': True})

def GenerateHorseKnots():
    Knot1 = random.normalvariate(8,1.5)
    Knot2 = random.normalvariate(8,1.5)
    Knot3 = random.normalvariate(8,1.5)
    Knot4 = random.normalvariate(8,1.5)
    Knot5 = random.normalvariate(9,1.5)
    Knot6 = random.normalvariate(13,4)
    return [Knot1, Knot2, Knot3, Knot4, Knot5, Knot6]

def GetHorseClass(currentClasses):
    # Instead subset the HorseClasses and choose from subset
    horse = random.choice(HorseClasses)
    while currentClasses and horse['Name'] in currentClasses:
        horse = random.choice(HorseClasses)
    return horse['Name']

@app.route('/Game/api/v1.0/SetHorses', methods=['GET','POST'])
def SetHorses():
    if(_ValidRequest(request)):
        desiredHorses = request.json['horsesCount']
        # Trim to current maximum number of different horses
        desiredHorses = min(desiredHorses, len(HorseClasses))

        # Init db
        db = database.get_db()
        # Get count of horses
        numberHorses = db.cursor().execute('SELECT COUNT(*) FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchone()[0]
        changed = False

        # add or remove horses
        if(numberHorses > desiredHorses):
            db.execute('DELETE FROM Horses WHERE id IN (SELECT id FROM Horses WHERE SessionId=? LIMIT ?)',[request.json['sessionId'],numberHorses-desiredHorses])
            db.commit()
            changed = True
        elif(numberHorses < desiredHorses):
            # Gt currently taken classes
            currentHorses = db.cursor().execute('SELECT HorseClass FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchall()
            # Add new horses 
            for i in range(0,desiredHorses - numberHorses):
                horseClass = GetHorseClass(currentHorses)
                db.execute('INSERT INTO Horses (SessionId, Name, HorseClass, Knot1, Knot2, Knot3, Knot4, Knot5, Knot6, ProbAction1, ProbAction2, Odds) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', 
	                            [request.json['sessionId'], horseClass, horseClass] + GenerateHorseKnots() + ["0","0","0"])
                db.commit()
                currentHorses.append(horseClass)
            changed = True

        # Get horses
        tbl_Horses = db.cursor().execute('SELECT Name, HorseClass, Knot1, Knot2, Knot3, Knot4, Knot5, Knot6, ProbAction1, ProbAction2 FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchall()

        if changed:
            BroadCastHorsesChanged(request.json['sessionId'])
        
        return jsonify({'Horses':[dict(x) for x in tbl_Horses]})
    
@app.route('/Game/api/v1.0/GetAllPlayers', methods=['GET','POST'])
def GetAllPlayers():
    if(_ValidRequest(request)):
        # Init db
        db = database.get_db()
        # Get all active players from game
        tbl_Players = db.cursor().execute('SELECT Alias, Standing FROM Users Where SessionId=?',[request.json['sessionId']]).fetchall()
        
        return jsonify({'Players':[dict(x) for x in tbl_Players]})

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

