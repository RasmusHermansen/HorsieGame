from HorsieServer.Setup import app, request, abort, socketio
from HorsieServer.views import BroadCastHorsesChanged, UpdateUserStanding, BroadCastRaceOver, BroadCastBettingDisabled, AdjustOdds
from HorsieServer.HorseClasses import HorseClasses
import HorsieServer.db as database
import datetime, random, string
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
    db.execute('INSERT INTO Sessions (SessionName, SessionKey, IsActive, BettingEnabled, Created) VALUES (?,?,1,1,?)', 
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
    Knot1 = random.normalvariate(12,2)
    Knot2 = random.normalvariate(8,1.5)
    Knot3 = random.normalvariate(7,1.5)
    Knot4 = random.normalvariate(8,1.5)
    Knot5 = random.normalvariate(10,1.5)
    Knot6 = random.normalvariate(14,3)
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
	                            [request.json['sessionId'], horseClass, horseClass] + GenerateHorseKnots() + ["0","0", str(desiredHorses)])
                db.commit()
                currentHorses.append(horseClass)
            changed = True

        # Get horses
        tbl_Horses = db.cursor().execute('SELECT id, Name, HorseClass, Knot1, Knot2, Knot3, Knot4, Knot5, Knot6, ProbAction1, ProbAction2 FROM Horses Where SessionId=?',[request.json['sessionId']]).fetchall()

        if changed:
            BroadCastHorsesChanged(request.json['sessionId'])
        
        return jsonify({'Horses':[dict(x) for x in tbl_Horses]})
    
@app.route('/Game/api/v1.0/GetAllPlayers', methods=['GET','POST'])
def GetAllPlayers():
    if(_ValidRequest(request)):
        # Init db
        db = database.get_db()
        # Get all active players from game
        tbl_Players = db.cursor().execute('SELECT Alias, Standing, id FROM Users Where SessionId=? AND IsActive=?',[request.json['sessionId'],True]).fetchall()
        
        return jsonify({'Players':[dict(x) for x in tbl_Players]})

@app.route('/Game/api/v1.0/DrinksDealt', methods=['GET','POST'])
def DrinksDealt():
    if(_ValidRequest(request)):
        # Init db
        db = database.get_db()
        # Set all drinks as dealt
        db.execute('UPDATE Drinks SET Dealt=? WHERE id=? AND SessionId=?', [True, request.json['drinkId'], request.json['sessionId']])
        db.commit()
        return jsonify({'Handled':True})

@app.route('/Game/api/v1.0/GetDrinks', methods=['GET','POST'])
def GetDealtDrinks():
    if(_ValidRequest(request)):
        # Init db
        db = database.get_db()
        # Get all unhandled drinks
        drinks = db.cursor().execute('SELECT id, FromUserId, ToUserId, Drink FROM Drinks Where SessionId=? AND Dealt=?',[request.json['sessionId'],False]).fetchall()
        # Return
        return jsonify({'Drinks':[dict(x) for x in drinks]})

@app.route('/Game/api/v1.0/GetActiveBets', methods=['GET','POST'])
def GetAllBets():
    raise NotImplementedError()

@app.route('/Game/api/v1.0/ReportResults', methods=['GET','POST'])
def ReportResults():
    if(_ValidRequest(request)):    
        sessId = request.json['sessionId']

        db = database.get_db()
        # Get unhandled all bets
        bets = db.cursor().execute('SELECT UserId, HorseId, Odds, Amount FROM Bets WHERE SessionId=? AND Handled=?',[sessId,False]).fetchall()

        # Make all unhandled bets handled
        db.execute('UPDATE Bets SET Handled=? WHERE SessionId=?', [True,sessId])
        db.commit()

        # Reward winners (Should aggregate)
        for row in bets:
            if row['HorseId'] == request.json['results'][0]:
                UpdateUserStanding(sessId, row['UserId'], row['Odds']*row['Amount'])

        BroadCastRaceOver(sessId, request.json['results'][:3])
        
        # Rescale Odds
        AdjustOdds(sessId, 2)

        # Re-enable betting
        SetBettingState(True, sessId)

        return jsonify({'Handled':True})

@app.route('/Game/api/v1.0/DisableBetting', methods=['GET','POST'])
def DisableBetting():
    if(_ValidRequest(request)):
        sessId = request.json['sessionId']

        SetBettingState(False, sessId)

        BroadCastBettingDisabled(sessId)

        return jsonify({'Handled':True})

@app.route('/Game/api/v1.0/RaceStarting', methods=['GET','POST'])
def RaceStarting():
    if(_ValidRequest(request)):
        sessId = request.json['sessionId']

        AdjustOdds(sessId, 0.5)

        return jsonify({'Handled':True})

@app.route('/Game/api/v1.0/AddPlayerFunds', methods=['GET','POST'])
def AddPlayerFunds():
    if(_ValidRequest(request)):
        sessId = request.json['sessionId']
        userId = request.json['userId']
        amount = request.json['amount']

        UpdateUserStanding(sessId, row['UserId'], row['Odds']*row['Amount'])
        return jsonify({'Handled':True})

def SetBettingState(state, sessId):
    db = database.get_db()
    db.execute('UPDATE Sessions SET BettingEnabled=? WHERE id=?',[state,sessId])
    db.commit()