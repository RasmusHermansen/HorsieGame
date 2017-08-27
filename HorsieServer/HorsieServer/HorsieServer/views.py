from HorsieServer.Setup import app, request, render_template, session, flash, redirect, url_for
import HorsieServer.db as database
import datetime
d = datetime.datetime.now()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Validate input
        if(len(request.form['Alias'])==0):
            error="Empty Alias"
        else:
            # Query db
            db = database.get_db()
            res = db.cursor().execute('SELECT id, IsActive FROM Sessions WHERE SessionName=?',[request.form['SessionId']]).fetchone()
            # Check existence of session
            if(len(res) == 0):
                error="Invalid session id"
            # Check if session is live
            elif(res["IsActive"] != 1):
                error="The session is no longer active"
            # Check if Alias already active
            elif(False):
                pass    
            # Enter session
            else:
                session['Alias'] = request.form['Alias']
                session['SessionId'] = res["id"]
                db.execute('INSERT INTO Users (SessionId, Alias, Standing) VALUES (?,?,?)', [res["id"],request.form['Alias'],10])
                db.commit()
                flash('You were entered in as: ' + session['Alias'])
                return redirect(url_for('GameInfo'))
    return render_template('index.html', error=error)

# Temp for dev
@app.route('/Game')
def GameInfo():
    # Check Session
    pass
    # Get Users
    db = database.get_db()
    tbUsers = db.cursor().execute('SELECT * FROM Users WHERE SessionId=?',[session['SessionId']]).fetchall()
    # Get tbHorses
    tbHorses = db.cursor().execute('SELECT * FROM Horses WHERE SessionId=?',[session['SessionId']]).fetchall()   
    return render_template('GameInfo.html', tbUsers=tbUsers, tbHorses=tbHorses)