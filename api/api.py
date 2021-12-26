# Pyauth REST API
# Made by the super cool, charasmatic and handsome aliisverymad, licensed under the MIT license.
# For more infomation, please check the github repository @ https://github.com/aliisverymad/pyauth

# Print Status codes
# print('[','\033[32mOK','\033[0m]: ')
# print('[','\033[34mINFO','\033[0m]: ')
# print('[','\033[31mERROR','\033[0m]: ')

# Start the very basic of libraries
import os
print("Initalising Pyauth")
print("Please wait...")
version = "1.0.0"

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

# Load main API settings from JSON file into memory
with open('apiconfig.json') as apiconfig:
    config = json.load(apiconfig)
    masterapikey = config.get('masterapikey')
    if masterapikey == "defaultkey":
        logo()
        print('[','\033[31mERROR','\033[0m]: Insecure master key warning!')
        print('[','\033[34mINFO','\033[0m]: Please change the master API key from default in apiconfig.json.')
        print('[','\033[34mINFO','\033[0m]: This prevents from bad actors from executing actions locked to the admin!')
        print('[','\033[34mINFO','\033[0m]: Pyauth will not launch until the key is changed')
        exit()
    else:
        pass
    usehwid = config.get('usehwidverification')
    allowoutdated = config.get('allowoutdatedconnections')
    allow2fa = config.get('use2FAverification')
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
    cur.execute('''select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('paUsers'));''')
    userdbcheck = cur.fetchall()
    cur.execute('''select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('paKeys'));''')
    keydbcheck = cur.fetchall()
    # If they do, continue. if they don't, error and create a DB and then continue
    for row in userdbcheck:
        print(row[0])
        if row[0] == True:
            print('[','\033[32mOK','\033[0m]: User authentication database exists!')
        elif row[0] == False:
            print('[','\033[31mERROR','\033[0m]: User authentication database not found!')
            print('[','\033[34mINFO','\033[0m]: Creating database...')
            cur.execute('''
    CREATE TABLE paUsers (
        apikey TEXT UNIQUE NOT NULL,
        email VARCHAR ( 255 ) UNIQUE NOT NULL,
        username VARCHAR ( 50 ) UNIQUE NOT NULL,
        password TEXT NOT NULL,
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
    for row in keydbcheck:
        if row[0] == True:
            print('[','\033[32mOK','\033[0m]: API Key database exists!')
        elif row[0] == False:
            print('[','\033[31mERROR','\033[0m]: API Key database not found!')
            print('[','\033[34mINFO','\033[0m]: Creating database...')
            cur.execute('''
    CREATE TABLE paKeys (
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

@app.route('/api/v2/auth/info', methods=['GET', 'POST'])
def serverinfo():
    return jsonify({"usehwid" : f"{usehwid}", "allowoutdated": f"{allowoutdated}", "allow2fa": f"{allow2fa}"})


logo()
print("Press CTRL+C to quit")
app.run(debug=True, use_reloader=False)
    