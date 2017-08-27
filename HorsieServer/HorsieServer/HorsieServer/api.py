from HorsieServer.Setup import app, request, abort
import HorsieServer.db as database
import datetime, random
from flask import jsonify

# TODO:
# REMOVE GET from methods for entire api
# Make key related to session (no troll)

@app.route('/Game/api/v1.0/CreateSession', methods=['GET','POST'])
def CreateSession():
    #replace sessionNames with valid generator
    sessionNames = ("Memes", "Krugge412", "BaNAn2", "test21241", "temp1213", "wololo2")
    
    sessionName = ""
    # Iterate new SessionNames untill valid
    while True:
        # Create SessionName
        sessionName = random.choice(sessionNames)
        # Check if it is unique and inactive
        sessId = database.ActiveSessionIdFromSessionName(sessionName)
        if(sessId == -1):
            break


    # Create Session
    db = database.get_db()
    db.execute('INSERT INTO Sessions (SessionName, IsActive, Created) VALUES (?,1,?)', 
	                    [sessionName,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    db.commit()
    # Get new sessionId
    return jsonify({'sessionName': sessionName, 'uniqueId': database.ActiveSessionIdFromSessionName(sessionName)})


@app.route('/Game/api/v1.0/CloseSession', methods=['GET','POST'])
def CloseSession():
    if not request.json:
        abort(400)
    sessId = request.json['SessionId']
    # Check if it is active
    if(database.SessionActive(sessId)):
        # Close Session
        db = database.get_db()
        db.execute('UPDATE Sessions SET IsActive = 0, Closed = ? WHERE id=?', 
	                        [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),sessId])
        db.commit()

    return jsonify({'Closed': True})