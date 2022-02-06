# pyauth server

from dataclasses import dataclass
from distutils.log import error
import os

print("Initalising Pyauth")
print("Checking for required libraries")
print("Please wait...")

try:
    from pahelper.console import *
    from pahelper.filemgmt import *
except:
    print("pyauth can not import its helper libraries! Please check that pyauth is installed correctly and updated to the latest version")

logo()
prntok("Loaded helper libraries!")
prntinfo("Checking for read/write permissisions")

getdir = os.getcwd()
readcheck = canread(getdir)
writecheck = canwrite(getdir)
if readcheck == True:
    prntok("Directory is readable!")
else:
    prnterror("pyauth can not read the current directory!")
    prnterror("how the hell r u running this :O")
    exit()
if writecheck == True:
    prntok("Directory is writable!")
    LocalSQLready = True
else:
    LocalSQLready = False
    prntwarn("pyauth can not write to the directory, SQLite functionality will be disabled.")

prntinfo("Loading all other libraries...")
try:
    from flask import Flask, redirect, render_template, request, jsonify, flash, url_for
    import psycopg2 as pgsql
    import sqlite3
    import secrets
    import webbrowser
    from datetime import datetime
    import hashlib
    import json
    import re
    import pyotp
    import threading
except:
    prnterror("Could not load pyauth libraries...")
    exit()


if LocalSQLready == True:
    prntinfo("Checking for any local disk databases...")
    dbfileexists = exists("database/dbconfig.db")
    if dbfileexists == True:
        prntinfo("Local database found!")
        prntinfo("Loading...")
        try:
            sqldb = sqlite3.connect('pyauthsettings.db')
        except:
            prnterror("Could not connect to this database!")
            prntinfo("Checking for a configuration file...")
            configfileexists = exists("dbconfig.json")
            if configfileexists == True:
                with open('dbconfig.json') as dbconfig:
                    config = json.load(dbconfig)
                    dbmode = config.get('databasemode')
                    database = config.get('pgdatabase')
                    username = config.get('pgusername')
                    password = config.get('pgpassword')
                    hostname = config.get('pghostname')
                    dbport = config.get('pgport')
                prntok("Config file found!")
                prntinfo("Checking connection details...")
                try:
                    pgdb = pgsql.connect(database=database, user=username, password=password, host=hostname, port=dbport)
                    prntok("Connected successfully!")
                    pgcur = pgdb.cursor()
                except:
                    prnterror("Failed to connect to the remote database!!!")
                    prnterror("pyauth cannot store data in a database that doesn't exist :facepalm:")
                    exit()
        prntok("Connected!")
        sqlcur = sqldb.cursor()
if LocalSQLready == False:
    prntinfo("Checking for a configuration file...")
    configfileexists = exists("dbconfig.json")
    if configfileexists == True:
        with open('dbconfig.json') as dbconfig:
            config = json.load(dbconfig)
            dbmode = config.get('databasemode')
            database = config.get('pgdatabase')
            username = config.get('pgusername')
            password = config.get('pgpassword')
            hostname = config.get('pghostname')
            dbport = config.get('pgport')
        prntok("Config file found!")
        prntinfo("Checking connection details...")
        try:
            pgdb = pgsql.connect(database=database, user=username, password=password, host=hostname, port=dbport)
            prntok("Connected successfully!")
            pgcur = pgdb.cursor()
        except:
            prnterror("Failed to connect to the remote database!!!")
            prnterror("pyauth cannot store data in a database that doesn't exist :facepalm:")
            exit()
else:
    prntwarn("No database or configuration file found!")
    prntinfo("Continuing in setup mode!")
    setup = True

# Flask preparation phase
logo()
prntinfo("Preparing Flask...")
app = Flask(__name__, static_url_path='/static')
app.secret_key = "wap"

# pyauth Web Panel setup routes start here --------------------------------------------------------------------------------------------------------------------------------X
prntinfo("Loading Setup routes...")
@app.route('/csetup', methods=['POST', 'GET'])
def wpsetup():
    if setup == True:
        return render_template("")



# pyauth Web Panel routes start here --------------------------------------------------------------------------------------------------------------------------------X
prntinfo("Loading Web Panel routes...")
@app.route('/controlpanel', methods=['GET', 'POST'])
def wplogin():
    if request.method == 'POST' and 'keyinput' in request.form:
        apikey = request.form['keyinput']
        if apikey == "123":
            return redirect(url_for("wphome"))
        else:
            print("error")
    return render_template("wplogin.html")

@app.route('/controlpanel/home', methods=['GET', 'POST'])
def wphome():
    return render_template("wphome.html")

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("wphome.html")

# pyauth authentication API routes start here --------------------------------------------------------------------------------------------------------------------------------------X
prntinfo("Loading API routes...")
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for("apiindex"))

@app.route('/api', methods=['GET', 'POST'])
def apiindex():
    return "API ONLINE", 200

# fucking hell this is v4 
@app.route('/api/v4/user/register', methods=['GET', 'POST'])
def userregister():
    totp = pyotp.TOTP(pyotp.random_base32())
    apikey = request.headers.get('apikey')
    email = request.headers.get('email')
    username = request.headers.get('username')
    password = request.headers.get('password')
    token = secrets.token_urlsafe(128)
    date = datetime.today().strftime('%Y-%m-%d')
    pgcur.execute('''''')
    
    






def threadlauncher():
    if setup == True:
        webbrowser.open("http://127.0.0.1:5000/controlpanel")
    app.run(debug=True, use_reloader=False)
servercontrol = threading.Thread(target=threadlauncher)

prntok("Finished!")
prntinfo("Launching pyauth using 1 thread...")


if __name__ == '__main__':
    threadlauncher()
else:
    try:
        servercontrol.start()
        servercontrol.join()
        prntok("Pyauth successfully launched!")
    except:
        prnterror("pyauth was unable to start...")
        exit()