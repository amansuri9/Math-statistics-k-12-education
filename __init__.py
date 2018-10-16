from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.utils import secure_filename
from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from allTabs import AllTabs
import os
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Connect to database
try:
    conn = pymysql.connect(host='cs358.cis.valpo.edu', port=3306,
                           user='schoolstat', passwd='schoolstat123', db='schoolstat')
except:
    print("\nIt looks like you can't connect to the cs358.cis.valpo.edu server.")
    print("Please change the database host to localhost in __init__.py:21 if you are running MathStats on the cs358 server or with a local MySQL instance.")
    print("It's possible to connect to the cs358 database from off-campus using SonicWall.")
    print("Valpo SonicWall instructions available at https://goo.gl/hafC4g.\n\n")
  
cur = conn.cursor()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
tabs = AllTabs()  # Will create a dataProcessor object with empty df and cat_indices


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Handle user logout."""
    tabs.clear_df() # clear any data that's been uploaded
    session.pop('username', None)
    if 'file' in session:
        try:
            os.remove(os.path.join(session['file']))  # delete file from server on logout
            session.pop('file', None)
        except:
            print("file not uploaded in this session")
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    error = request.args.get('error') or None
    if request.method == 'POST':
        try:
            cur.execute(
                "SELECT * from users where username = \"" + request.form['username'] + "\" and password = SHA(\'" +
                request.form['passwd'] + "\')")
            # Error messaging
            if request.form['username'] == '':
                error = 'No username entered'
            if request.form['passwd'] == '':
                error = 'No username or password entered'
            elif request.form['passwd'] == '':
                error = 'No password entered'
            elif request.form['passwd'].find(")") != -1 or request.form['passwd'].find("\'") != -1 or \
                    request.form['passwd'].find(";") != -1 or request.form['passwd'].find("\"") != -1:
                error = 'Nice try'
            elif cur.rowcount == 0:
                error = 'Invalid username or password'
                print("Invalid username or password")
            # End error messaging
            elif cur.rowcount > 0 and not ('username' in session):
                session['username'] = request.form['username']
                print("login successful")
                return redirect('')
            else:
                print("error in login")
        except:
            error = 'Nice try'
    return render_template('login.html', error=error)


@app.route('/')
def homepage():
    """Set up homepage and connect to the bokeh server."""
    # Pull from Bokeh Server:
    URL = "http://localhost:5006"
    script = server_document(URL)

    # Verify login and load main.html
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("main.html", bokehSession=script, template="Flask")


def allowed_file(filename):
    """Check that the file has the proper extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads. Starts a bokeh server when a file is uploaded properly."""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # check that the user wasn't already working with a file, and if so, delete it from server
            if 'file' in session:
                try:
                    os.remove(os.path.join(session['file']))
                except:
                    print("file not found")
            # Name file properly
            cur.execute("SELECT id from users where username = \"" + session['username'] + "\"")
            filename = secure_filename(file.filename.replace(".csv", datetime.now().strftime(
                '%Y-%m-%d%H-%M-%S') + 'userid' + str(cur.fetchone()).replace("(", "").replace(",)", "") + ".csv"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['file'] = UPLOAD_FOLDER + '/' + filename

            # pass csv to AllTabs to pass to DataProcessor (populates DataProcessor with data from file)
            tabs.update_df(session['file'])

            # Start bokeh server only after a file has been uploaded
            from threading import Thread
            Thread(target=bk_worker).start()

            return redirect(request.url)

        return redirect(url_for('upload_file'))


def bk_worker():
    """Start bokeh server on port 5006"""
    server = Server({'/': Application(FunctionHandler(tabs.runServer))}, io_loop=IOLoop(), port=5006,
                    allow_websocket_origin=["*"])
    server.start()
    server.io_loop.start()


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))  # Start Flask server

cur.close()
conn.close()
