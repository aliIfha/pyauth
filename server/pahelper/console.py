import os

def cls():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def prntok(string):
    print('[','\033[32mOK',f'\033[0m]: {string}')

def prnterror(string):
    print('[','\033[31mERROR',f'\033[0m]: {string}')

def prntwarn(string):
    print('[','\033[33mWARN',f'\033[0m]: {string}')

def prntinfo(string):
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