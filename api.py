import os
from flask import Flask, render_template, request, jsonify
import psycopg2
import secrets
from datetime import datetime
import hashlib

# PostgreSQL Configuration options. Will add mongoDB support later
database = "d6up96j3u24eu"
username = "pmgorumxuvcmpi"
password = "038dc3a46337d191384fc0d909aa4bb84fb5c02ab9ca95932ac65429b2ef1294"
hostname = "ec2-18-202-67-49.eu-west-1.compute.amazonaws.com"
dbport = "5432"

# API Configuration Options
masterapikey = 'e46d0ec5-c753-4ef9-997f-0f2d592b7e23' # Do not share with anyone.
imbored = "wip do this later"

db = psycopg2.connect(database=database, user=username, password=password, host=hostname, port=dbport)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'API ONLINE', 200

@app.route('/api/v1/internal/createapikey', methods=['GET', 'POST'])
def createapikey():
    inputkey = request.headers.get('Authorization')
    if inputkey == masterapikey:
        apikey = secrets.token_urlsafe(64)
        return jsonify({"apikey" : apikey})
    else:
        return 'NOT ALLOWED', 405

@app.route('/api/v1/user/create', methods=['GET', 'POST'])
def createaccount():
    apikey = request.headers.get('key')
    email = request.headers.get('email')
    username = request.headers.get('username')
    password = request.headers.get('password')
    hwid = request.headers.get('hwid')
    date = datetime.today().strftime('%Y-%m-%d')
    token = secrets.token_urlsafe(128)
    print(apikey, email, username, password, hwid, date, token)
    cur = db.cursor()
    cur.execute(f"SELECT * FROM validapikeys WHERE apikey = '{apikey}'")
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
        if apikey == row[0]:
            print("success!")
            cur.execute(f"DELETE FROM validapikeys WHERE apikey = '{apikey}'")
            cur.execute(f"INSERT INTO userdetails (apikey,email,username,password,tiedhwid,created_on,last_login,token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (apikey, email, username, password, hwid, date, date, token))
            db.commit()
            return jsonify({"token" : token}), 200
        else:
            return 'NOT ALLOWED', 405

@app.route('/api/v1/user/auth', methods=['GET', 'POST'])
def auth():
    email = request.headers.get('email')
    password = request.headers.get('password')
    hwid = request.headers.get('hwid')
    print(email)
    print(password)
    print(hwid)

    cur = db.cursor()
    cur.execute(f"SELECT * FROM userdetails WHERE email = '{email}'")
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
        if email == row[0]:
            cur.execute(f"SELECT * FROM userdetails WHERE password = '{password}'")
            rows = cur.fetchall()
            salt = row[0][:32]
            key = row[0][32:]
            passtocheck = hashlib.pbkdf2_hmac('sha256', key.encode('utf-8'), salt, 100000)
            print(password)
            print(passtocheck)
            if password == passtocheck:
                cur.execute(f"SELECT * FROM userdetails WHERE tiedhwid = '{hwid}'")
                cur.fetchall()
                if hwid == row[0]:
                    cur.execute(f"SELECT token FROM userdetails WHERE email = '{email}'")
                    cur.fetchall()
                    return jsonify({"token" : row[0]}), 200
                else:
                    return 'NOT ALLOWED', 405
            else:
                return 'NOT ALLOWED', 405
        else:
            return 'EMAIL DOES NOT EXIST, IMAGINE LMAO', 404


def launch():
    app.run(debug=True)
    print("running\npress any key to stop")
    os.system('pause')

launch()