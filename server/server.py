# pyauth server

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
    exit()
if writecheck == True:
    prntok("Directory is writable!")
else:
    prntwarn("pyauth can not write to the directory, SQLite functionality will be disabled.")

prntinfo("Loading all other libraries...")
try:
    from flask import Flask, redirect, render_template, request, jsonify, flash, url_for
    import psycopg2
    import sqlite3
    import secrets
    from datetime import datetime
    import hashlib
    import json
    import re
    import pyotp
    import threading
except:
    prnterror("Could not load pyauth libraries...")
    exit()


configfile = exists("dbconfig.json")
if configfile == True:
    prntok("Configuration file exists, loading settings...")
    masterkey = readconfig("masterapikey")
    if masterkey == "defaultkey":
        logo()
        prnterror("Change the default master key.")
        exit()
    else:
        pass
else:
    prntinfo("Configuration file doesn't exist!")
    if writecheck == True:
        prntinfo("Creating one...")
        createconfig()
    else:
        prnterror("pyauth doesn't have access to the current directory. Please give write permissions or create a configuration profile before running.")
        exit()

# Flask preparation phase
logo()
prntinfo("Preparing Flask...")
app = Flask(__name__, static_url_path='/static')
app.secret_key = "wap"

# pyauth API routes start here --------------------------------------------------------------------------------------------------------------------------------------X
prntinfo("Loading API routes...")
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for("wplogin"))

@app.route('/api', methods=['GET', 'POST'])
def register():
    pass

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



def threadlauncher():
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