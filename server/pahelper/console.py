import os
from datetime import date

def cls():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def log(input):
    today = date.today()
    filename = today.strftime("%d%m%Y")
    filecheck = os.access(f"{filename}.log", os.F_OK)
    if filecheck == True:
        pass
    else:
        with open(f"{filename}.log", "w") as f:
            f.close
    with open(f"{filename}.log", "a") as logger:
        logger.write(input)

def prntok(string):
    log(f"[ OK ]: {string}\n")
    print('[','\033[32mOK',f'\033[0m]: {string}')

def prnterror(string):
    log(f"[ ERROR ]: {string}\n")
    print('[','\033[31mERROR',f'\033[0m]: {string}')

def prntwarn(string):
    log(f"[ WARN ]: {string}\n")
    print('[','\033[33mWARN',f'\033[0m]: {string}')

def prntinfo(string):
    log(f"[ INFO ]: {string}\n")
    print('[','\033[34mINFO',f'\033[0m]: {string}')

def timeout(time):
    time.sleep(time)

def logo():
    cls()
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

def pause():
    os.system('pause')