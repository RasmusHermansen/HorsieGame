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


@app.route('/Game/api/v1.0/CloseSession', methods=['GET','POST'])
def CloseSession():
    if not request.json:
        abort(400)
    sessId = request.json['sessionId']
    sessKey = request.json['sessionKey']
    # Check if it is active and correct key
    if(database.SessionActive(sessId) and database.CorrectSessionKey(sessId, sessKey)):
        # Close Session
        db = database.get_db()
        db.execute('UPDATE Sessions SET IsActive = 0, Closed = ? WHERE id=?', 
	                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),sessId])
        db.commit()

    return jsonify({'Closed': True})