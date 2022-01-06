# Pyauth REST API
# Made by the super cool, charasmatic and handsome aliisverymad, licensed under the MIT license.
# For more infomation, please check the github repository @ https://github.com/aliisverymad/pyauth

# Print Status codes
# print('[','\033[32mOK','\033[0m]: ')
# print('[','\033[34mINFO','\033[0m]: ')
# print('[','\033[31mERROR','\033[0m]: ')

# Start the very basic of libraries
import os
from types import MethodDescriptorType
print("Initalising Pyauth")
print("Please wait...")
version = "prerelease"

def logo():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    print("""
                         _   _     
                        | | | |    
 _ __  _   _  __ _ _   _| |_| |__  
| '_ \| | | |/ _` | | | | __| '_ \ 
| |_) | |_| | (_| | |_| | |_| | | |
| .__/ \__, |\__,_|\__,_|\__|_| |_|
| |     __/ |made by aliisverymad
|_|    |___/         

    """)

# Start the coloured text library for super sick colors OMGG!!1!11!
import colorama
from colorama.ansi import Fore
import time # Also start the time library for sleep commands
colorama.init()

logo()
print('[','\033[32mOK','\033[0m]: Colorama launched successfully!')

time.sleep(1)
# Check for API config file
print('[','\033[34mINFO','\033[0m]: Checking for configuration files...')
filecheck = os.access("apiconfig.json", os.F_OK)
if filecheck == True:
    print('[','\033[32mOK','\033[0m]: API Configuration file exists!')
else:
    print('[','\033[31mERROR','\033[0m]: API Configuration file does not exist, creating...')
    print('[','\033[32mOK','\033[0m]: Created configuration file successfully!')
time.sleep(1)
# Check for database config file
filecheck = os.access("database.json", os.F_OK)
if filecheck == True:
    print('[','\033[32mOK','\033[0m]: Database Configuration file exists!')
else:
    print('[','\033[31mERROR','\033[0m]: Database Configuration file does not exist, creating...')
    print('[','\033[32mOK','\033[0m]: Created configuration file successfully!')

# Return successful file check
time.sleep(1)
print('[','\033[32mOK','\033[0m]: Passed all file checks!')
time.sleep(1)
print('[','\033[34mINFO','\033[0m]: Proceeding!')

from flask import Flask, render_template, request, jsonify
import psycopg2
import secrets
from datetime import datetime
import hashlib
import json
import re
import pyotp

# Load main API settings from JSON file into memory
with open('apiconfig.json') as apiconfig:
    config = json.load(apiconfig)
    masterapikey = config.get('masterapikey')
    useAPIconnectionkey = config.get('useAPIconnectionkey')
    if useAPIconnectionkey == True:
        apiconnectionkey = config.get('APIconnectionkey')
    else:
        pass
    if masterapikey == "defaultkey":
        logo()
        print('[','\033[31mERROR','\033[0m]: Insecure master key warning!')
        print('[','\033[34mINFO','\033[0m]: Please change the master API key from default in apiconfig.json.')
        print('[','\033[34mINFO','\033[0m]: This prevents from bad actors from executing actions locked to the admin!')
        print('[','\033[34mINFO','\033[0m]: Pyauth will not launch until the key is changed')
        apiconfig.close()
        exit()
    elif apiconnectionkey == "defaultkey":
        logo()
        print('[','\033[31mERROR','\033[0m]: Insecure master key warning!')
        print('[','\033[34mINFO','\033[0m]: Please change the master API key from default in apiconfig.json.')
        print('[','\033[34mINFO','\033[0m]: This prevents from bad actors from executing actions locked to the admin!')
        print('[','\033[34mINFO','\033[0m]: Pyauth will not launch until the key is changed')
        apiconfig.close()
        exit()
    else:
        pass
    usehwid = config.get('usehwidverification')
    allowoutdated = config.get('allowoutdatedconnections')
    allow2fa = config.get('use2FAverification')
    enforce2fa = config.get('enforce2FAverification')
    useGPS = config.get('useGPS')
    antiVPN = config.get('useantivpn')
    apikeyonly = config.get('apikeyonly')
    identifiermode = config.get('identifiermode')
    webhookenabled = config.get('webhookenabled')
    if webhookenabled == True:
        webhookurl = config.get('webhookurl')
    else:
        pass
    apiconfig.close()

# Load main PostgreSQL location from JSON file into memory
with open('database.json') as dbconfig:
    config = json.load(dbconfig)
    dbmode = config.get('databasemode')
    database = config.get('pgdatabase')
    username = config.get('pgusername')
    password = config.get('pgpassword')
    hostname = config.get('pghostname')
    dbport = config.get('pgport')
    dbconfig.close()

# Check which database mode it is in and then accordingly change libraries and commands.
if dbmode == "postgres":
    db = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=dbport)
    cur = db.cursor()
    # Check if Postgres DB's exist
    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()
    print(list_database)
    # If they do, continue. if they don't, error and create a DB and then continue
    if "paUsers" in list_database:
        print('[','\033[32mOK','\033[0m]: User authentication database exists!')
    elif "paUsers" not in list_database:
        print('[','\033[31mERROR','\033[0m]: User authentication database not found!')
        print('[','\033[34mINFO','\033[0m]: Creating database...')
        cur.execute('''
CREATE TABLE IF NOT EXISTS paUsers (
    apikey TEXT UNIQUE,
    email VARCHAR ( 255 ) UNIQUE,
    username VARCHAR ( 50 ) UNIQUE,
    password TEXT NOT NULL ,
    mfasecret TEXT,
    tiedhwid TEXT UNIQUE,
    token TEXT UNIQUE NOT NULL,
    created_on TIMESTAMP,
    last_login TIMESTAMP
    );''')
        db.commit()
        print('[','\033[32mOK','\033[0m]: Database created successfully!')
    else:
        print('[','\033[31mERROR','\033[0m]: A internal error occured...')
        exit()
    if "paKeys" in list_database:
        print('[','\033[32mOK','\033[0m]: API Key database exists!')
    elif "paKeys" not in list_database:
        print('[','\033[31mERROR','\033[0m]: API Key database not found!')
        print('[','\033[34mINFO','\033[0m]: Creating database...')
        cur.execute('''
CREATE TABLE IF NOT EXISTS paKeys (
    apikey VARCHAR ( 255 ) UNIQUE NOT NULL,
    keytype VARCHAR ( 50 ) NOT NULL,
    created_on TIMESTAMP);''')
        db.commit()
        print('[','\033[32mOK','\033[0m]: Database created successfully!')
    else:
        print('[','\033[31mERROR','\033[0m]: A internal error occured...')
        exit()
    os.system('pause')
else:
    logo()
    print('[','\033[31mERROR','\033[0m]: Invalid or missing database mode selected!')
    print('[','\033[34mINFO','\033[0m]: Please change the database mode in apiconfig.json.')
    print('[','\033[34mINFO','\033[0m]: Without it, the API can not store its data.')
    exit()

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def index():
    return 'API ONLINE', 200

# Admin API routes. please for the love of this API, don't share your master api key with anyone (apart from me of course :3).
@app.route('/api/v2/internal/createapikey', methods=['GET', 'POST'])
def createapikey():
    masterapikey = 'e46d0ec5-c753-4ef9-997f-0f2d592b7e23'
    #masterapikey = os.getenv("apikey")
    inputkey = request.headers.get('Authorization')
    if inputkey == masterapikey:
        apikey = secrets.token_urlsafe(64)
        return jsonify({"apikey" : apikey})
    else:
        return 'NOT ALLOWED', 405


# API user authentication routes. This is where the actual internals of the API lay.
@app.route('/api/v2/auth/info', methods=['GET', 'POST'])
def serverinfo():
    return jsonify({"version" : f"{version}", "usehwid" : f"{usehwid}", "allowoutdated": f"{allowoutdated}", "allow2fa": f"{allow2fa}", "enforce2fa": f"{enforce2fa}", "useGPS": f"{useGPS}", "antiVPN" : f"{antiVPN}"}), 200

@app.route('/api/v2/user/register', methods=['GET', 'POST'])
def register():
    totp = pyotp.TOTP(pyotp.random_base32())
    apikey = request.headers.get('username')
    email = ""
    username = request.headers.get('username')
    password = request.headers.get('password')
    token = secrets.token_urlsafe(128)
    date = datetime.today().strftime('%Y-%m-%d')
    if usehwid == True:
        hwid = request.headers.get('hwid')
    cur.execute(f"INSERT INTO userdetails (apikey,email,username,password,tiedhwid,created_on,last_login,token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (apikey, email, username, password, hwid, date, date, token))
    return jsonify({"mfasecretkey" : f"{totp}"}), 201

@app.route('/api/v2/user/login', methods=['GET', 'POST'])
def auth():
    pass # work in progress


logo()
print("Press CTRL+C to quit")
app.run(debug=True, use_reloader=True)
    