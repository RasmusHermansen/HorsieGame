import sqlite3
from HorsieServer.Setup import app, g

def connect_db():
    """Connects to the db"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def SessionActive(sessionId):
    res = get_db().cursor().execute('SELECT IsActive FROM Sessions WHERE id=?',[sessionId]).fetchone()
    if(res == None):
        return False
    return res['IsActive'] == 1

def ActiveSessionIdFromSessionName(sessionName):
    res = get_db().cursor().execute('SELECT id FROM Sessions WHERE SessionName=? AND IsActive=?',[sessionName,1]).fetchone()
    if(res == None):
        return -1
    return res['id']

def CorrectSessionKey(sessionId, sessionKey):
    res = get_db().cursor().execute('SELECT SessionKey FROM Sessions WHERE id=?',[sessionId]).fetchone()
    if(res == None or res['SessionKey'] != sessionKey):
        return False
    return True

def AllowUserToEnterActiveSession(sessionId, alias, userKey):
    res = get_db().cursor().execute('SELECT UserKey, IsActive FROM Users WHERE SessionId=? AND Alias=?',[sessionId,alias]).fetchone()
    if(res == None or res['IsActive'] == 0 or res['userKey'] == userKey):
        return True
    return False