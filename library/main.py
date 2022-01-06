# Made by ali#1000
import requests
import subprocess
import os
import hashlib

version = "prerelease"

# define API URL for library to contact. Make sure that its the url its self and doesn't include any routes.

def probe(url):
    r = requests.get(f"{url}api/v2/auth/info")
    global usehwid
    usehwid = r.json()['usehwid']
    global sversion
    sversion = r.json()['version']
    global allowoutdated
    allowoutdated = r.json()['allowoutdated']
    global allow2fa
    allow2fa = r.json()['allow2fa']
    global enforce2fa
    enforce2fa = r.json()['enforce2fa']
    global useGPS
    useGPS = r.json()['useGPS']
    global antiVPN
    antiVPN = r.json()['antiVPN']

def register(username, password, apiURL):
    if usehwid == True:
        # Windows support only, linux/macOS support coming soon maybe.
        cmd = 'wmic csproduct get uuid'
        uuid = str(subprocess.check_output(cmd))
        pos1 = uuid.find("\\n")+2
        uuid = uuid[pos1:-15]
    else:
        uuid = "null"
        pass
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    epassword = salt + key
    headers={"username": f"{username}", "password": f"{epassword}", "hwid": f"{uuid}"}
    r = requests.post(apiURL, headers=headers)
    if r.status_code == 201:
        token = r.json()['token']
        return "yay it worked!!!"
    elif r.status_code == 404:
        return "server returned 'not found'"
    elif r.status_code == 403:
        return "uh oh stinky. looks like you, ma boi, dont have access rights to this resource"
    else:
        return "something went wrong. :'("



def auth():
    if usehwid == True:
        cmd = 'wmic csproduct get uuid'
        uuid = str(subprocess.check_output(cmd))
        pos1 = uuid.find("\\n")+2
        uuid = uuid[pos1:-15]
    else:
        pass
    if allowoutdated == True:
        global versioncheck
        if version == sversion:
            versioncheck = 1
        else:
            versioncheck = 0
    else:
        pass
    if allow2fa == True:
        pass
    else:
        pass
    if antiVPN == True:
        pass
    else:
        pass