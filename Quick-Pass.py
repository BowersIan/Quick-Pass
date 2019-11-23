#import hashlib
import sys
import os
#import configparser
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import argparse
import clipboard
from getpass import getpass
import sqlite3
import base64

def encryptstring(string):
    if len(string)%16 != 0:
        print(string)
        for i in range (0,16-len(string)%16):
            string=string+'|'
    #print(len(string))   
    return base64.b64encode(enc.encrypt(string))

def decryptstring(string):
    #print(string.encode('ISO-8859-1'))
    return enc.decrypt(base64.b64decode(string))

def hashpassword(pwd):
    hsh = SHA256.new()
    hsh.update(pwd)
    return hsh.digest()

def makeDB():
    cursor.execute('CREATE TABLE PASS(SITE TEXT, USERNAME TEXT, PASSWORD BLOB);')
    DB.commit()

def isUpdate(site, usr):
    cursor.execute('SELECT * FROM PASS WHERE SITE = ? AND USERNAME = ?;',(site, usr))
    row = cursor.fetchone()
    return row is not None

def updatePassword(site, usr, pss):
    cursor.execute('UPDATE PASS SET PASSWORD = ? WHERE SITE = ? AND USERNAME = ?;',(pss, site, usr))
    DB.commit()
    
def addPassword(site, usr, pss):
    cursor.execute('INSERT INTO PASS (SITE, USERNAME, PASSWORD) VALUES(?,?,?);',(site, usr, pss))
    DB.commit()
    
def findRecords(site):
    cursor.execute('SELECT * FROM PASS WHERE SITE = ?;',(site,))
    return cursor.fetchall()
    
def outputPassword(pss):
    #enc = AES.new(hsh, AES.MODE_CBC, 'IV256 0987654321')
    password = decryptstring(pss)
    p1 = password.decode('ISO-8859-1').rstrip('|')
    if args.c:
        clipboard.copy(p1)
        print('Password copied to clipboard')
    else:
        print(p1)

parser=argparse.ArgumentParser()
parser.add_argument('-a', help='Add or update password', action='store_true')
parser.add_argument('-c', help='Copy password to clipboard. Requires the clipboard module to be installed', action='store_true')
parser.add_argument('filepath', help='Path to your passwords file. If not supplied will create/overwrite Data.db', nargs='?')

args=parser.parse_args()

#find or make config file
#config = configparser.ConfigParser()


#createFile = False
if not sys.stdin.isatty():
    temp=sys.stdin.read().split()
elif args.filepath is None and not args.a:
    print('Error: No datafile provided.')
elif args.filepath is not None:
    with open(args.filepath, 'rb') as f:
        temp=f.read().decode('ISO-8859-1').splitlines()
else:
    args.filepath = 'Data.db'
    temp=[]
    
    
pwd = getpass('Password: ')


if not os.path.isfile(args.filepath):
    DB = sqlite3.connect(args.filepath)
    cursor = DB.cursor()
    makeDB()
else:
    DB = sqlite3.connect(args.filepath)
    cursor = DB.cursor()



hsh = hashpassword(pwd.encode('utf-8'))




#passList = []
#for line in temp:
    #passList.append(line.split('||'))
    
#print(passList)

#Add password logic

if args.a:
    site = input('Enter sitename: ')
    username = input('Enter username: ')
    check = False
    while not check:
        password = getpass('Enter password: ')
        passwordcheck = getpass('Enter password again: ')
        if password == passwordcheck:
            check = True
        else:
            print('Passwords do not match! Try again.')
    enc = AES.new(hsh, AES.MODE_CBC, 'IV256 0987654321')
    password = encryptstring(password)
    
    
    if isUpdate(site, username):
        updatePassword(site, username, password)
    else:
        addPassword(site, username, password)    
    
    
    
#find password
else:
    site = input('Enter sitename: ')
    
    
    #result is of type list
    result = findRecords(site)
    DB.close()
    
    
    if len(result)>1:
        username = input('Enter username: ')
        check = False
        for rec in result:
            if rec[1]==username:
                pss=rec[2]
                check=True
                break
        if not check:
            print('Username not found.')
            sys.exit(0)
    
    elif len(result)==1:
        pss = result[0][2]
    else:
        print('Site not found.')
        sys.exit(0)
        
    enc = AES.new(hsh, AES.MODE_CBC, 'IV256 0987654321')
    outputPassword(pss)
try:
    DB.close()
except:
    pass
