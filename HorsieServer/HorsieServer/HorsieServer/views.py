from HorsieServer.Setup import app, request, render_template, session, flash, redirect, url_for
import HorsieServer.db as database
import datetime

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
            # Check if Alias already active in session
            elif(False):
                pass    
            # Enter session
            else:
                session['Alias'] = request.form['Alias']
                session['SessionId'] = sessId
                db = database.get_db()
                db.execute('INSERT INTO Users (SessionId, Alias, Standing) VALUES (?,?,?)', [sessId,request.form['Alias'],10])
                db.commit()
                flash('You were entered in as: ' + session['Alias'])
                return redirect(url_for('GameInfo'))
    return render_template('index.html', error=error)

# Temp for dev
@app.route('/Game')
def GameInfo():
    # Check Session
    if(not database.SessionActive(session['SessionId'])):
        return render_template('index.html', error="Inactive session supplied")
    # Get Users
    db = database.get_db()
    tbUsers = db.cursor().execute('SELECT * FROM Users WHERE SessionId=?',[session['SessionId']]).fetchall()
    # Get tbHorses
    tbHorses = db.cursor().execute('SELECT * FROM Horses WHERE SessionId=?',[session['SessionId']]).fetchall()   
    return render_template('GameInfo.html', tbUsers=tbUsers, tbHorses=tbHorses)