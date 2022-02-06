import os
import json
def exists(file):
    filecheck = os.access(file, os.F_OK)
    return filecheck

def canread(file):
    readcheck = os.access(file, os.R_OK)
    return readcheck

def canwrite(file):
    writecheck = os.access(file, os.W_OK)
    return writecheck

def createconfig():
    with open("dbconfig.json", 'w+') as config:
        config.write('''
{
    "masterapikey": "defaultkey1",
    "placeholder": "placeholder"

    "pghost": "hostname",
    "pgdb": "database",
    "pguser": "username",
    "pgpass": "password",
    "pgport": "portnumber"
}
''')

def readconfig(key):
    with open("dbconfig.json") as f:
        config = json.load(f)
        value = config.get(key)
        return value

def createfile(filename):
    with open(filename, "w") as f:
        f.close