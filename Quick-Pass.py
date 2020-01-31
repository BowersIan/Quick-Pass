#!/usr/bin/env python3
#Quick-Pass.py
#By Ian Bowers
#Easy to use, local only, password manager
#Version v1.1.0


import sys
import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import argparse
try:
    import clipboard
except:
    pass
from getpass import getpass
import sqlite3
import base64

#Requests the encryption passphrase from the user, then returns the SHA256 hash of it
def getDecryptionPassword():
    pwd = getpass('Encryption Passphrase: ')
    hsh = hashpassword(pwd.encode('utf-8'))
    return hsh

#Modifies password to be a multiple of 16, then returns the encrypted strings
def encryptstring(string):
    if len(string)%16 != 0:
        for i in range (0,16-len(string)%16):
            string=string+'|'
    hsh=getDecryptionPassword()
    encrypters=getEncrypter(hsh, 2)
    return [base64.b64encode(encrypters[0].encrypt(string)), base64.b64encode(encrypters[1].encrypt(hsh))]
    
#Generates and returns the specified number of encryption objects
def getEncrypter(hsh, num=1):
    returnset=[]
    while num>0:
        returnset.append(AES.new(hsh, AES.MODE_CBC, 'IV256 0987654321'))
        num-=1
    return returnset

#Decrypts the given string with the given hashed passphrase and returns the decrypted string
def decryptstring(string, hsh):
    return getEncrypter(hsh)[0].decrypt(base64.b64decode(string))

#Returns the given string as a SHA256 hash
def hashpassword(pwd):
    hsh = SHA256.new()
    hsh.update(pwd)
    return hsh.digest()

def makeDB():
    cursor.execute('CREATE TABLE PASS(SITE TEXT, USERNAME TEXT, PASSWORD BLOB, KEY BLOB);')
    DB.commit()
    
#Adds the Key column to PASS table if it does not already exist
def upgradeDB():
    try:
        cursor.execute('ALTER TABLE PASS ADD COLUMN KEY BLOB;')
        DB.commit()
        print('DB upgraded to v1.1.0')
    except sqlite3.OperationalError as e:
        print('DB already at v1.1.0')

#Returns True if the given Site, Username pair already exists in the database, false otherwise
def isUpdate(site, usr):
    cursor.execute('SELECT * FROM PASS WHERE SITE = ? AND USERNAME = ?;',(site, usr))
    row = cursor.fetchone()
    return row is not None

#Updates an already existing password in the database
def updatePassword(site, usr, pss, key):
    cursor.execute('UPDATE PASS SET PASSWORD = ?, KEY = ? WHERE SITE = ? AND USERNAME = ?;',(pss, key, site, usr,))
    DB.commit()
    
#Adds a new record to the database
def addPassword(site, usr, pss, key):
    cursor.execute('INSERT INTO PASS (SITE, USERNAME, PASSWORD, KEY) VALUES(?,?,?,?);',(site, usr, pss, key))
    DB.commit()
    
#Returns all records for a given site
def findRecords(site):
    cursor.execute('SELECT * FROM PASS WHERE SITE = ?;',(site,))
    return cursor.fetchall()
    
#Returns all Site, Username pairs
def findAllRecords():
    cursor.execute('SELECT SITE, USERNAME FROM PASS')
    return cursor.fetchall()

#Removes a given record from the database
def removeRecord(site, usr):
    cursor.execute('DELETE FROM PASS WHERE SITE = ? and USERNAME = ?;',(site, usr))
    DB.commit()

#Decrypts the given encrypted, hashed passphrase and checks it against the used decryption key
def checkPassphrase(hsh, hshkey):
    key = decryptstring(hshkey, hsh)
    return hsh == key


#Handles outputting of password
def outputPassword(pss, hshkey):
    
    hsh=getDecryptionPassword()
    if hshkey is not None and not checkPassphrase(hsh, hshkey):
        print('Incorrect passphrase!')
    else:
        password = decryptstring(pss, hsh)
        p1 = password.decode('ISO-8859-1').rstrip('|')
        if args.c and not args.no_copy:
            try:
                clipboard.copy(p1)
                print('Password copied to clipboard')
            except:
                print(p1)
        else:
            print(p1)
        
def getUsername():
    if args.u is None:
        username = input('Enter username: ')
    else:
        username = args.u
    return username

def getSiteName():
    if args.s is None:
        site = input('Enter sitename: ')
    else:
        site = args.s
    return site

def getPassword():
    if args.p is None:
        check = False
        while not check:
            password = getpass('Enter password: ')
            passwordcheck = getpass('Enter password again: ')
            if password == passwordcheck:
                check = True
            else:
                print('Passwords do not match! Try again.')
    else:
        password = args.p
        
    return password

parser=argparse.ArgumentParser()
parser.add_argument('-a', help='Add or update password', action='store_true')
parser.add_argument('-c', help='Copy password to clipboard. Requires the clipboard module to be installed; if not installed, this argument is ignored', action='store_true')
parser.add_argument('--no-copy', help='Overides -c and prints password to standard out', action='store_true')
parser.add_argument('-u', help='Specify the username for the specific site so you will not be asked if more than one record is found for the site. Ignored if there is only one record listed for the site.')
parser.add_argument('-s', help='Specify the site to retrieve the password from so you will not be asked')
parser.add_argument('-p', help='Specify the password to manage. If not specified, will be asked for. Not recommended to use as password will be stored in command history and visible to anyone watching.')
parser.add_argument('filepath', help='Path to your passwords file. If not supplied will create/overwrite ./Data.db', nargs='?', default='Data.db')
parser.add_argument('-z','-l', help='List known site and username combinations', action='store_true')
parser.add_argument('-r', help='Removes selected site and usernaname combination', action='store_true')
parser.add_argument('--upgrade', help='Upgrades your database for a newer version of Quick-Pass', action='store_true')

args=parser.parse_args()


if not os.path.isfile(args.filepath):
    DB = sqlite3.connect(args.filepath)
    #curser is needed to run makeDB
    cursor = DB.cursor()
    makeDB()
else:
    DB = sqlite3.connect(args.filepath)
    cursor = DB.cursor()
    
if args.upgrade:
    upgradeDB()

#Print all records
if args.z:
    for rec in findAllRecords():
        print(rec)
        
#Add password logic
if args.a:
    site = getSiteName()
    username = getUsername()
    password = getPassword()
    
    password_key = encryptstring(password)
    #print(password_key)
    if isUpdate(site, username):
        updatePassword(site, username, password_key[0], password_key[1])
    else:
        addPassword(site, username, password_key[0], password_key[1])    
    DB.close()
    
elif args.r:
    site = getSiteName()
    username = getUsername()
    removeRecord(site, username)
    DB.close()
#find password
else:
    
    
    site = getSiteName()   
    
    result = findRecords(site)
    DB.close()
    
    
    if len(result)>1:
        username = getUsername()
        check = False
        for rec in result:
            if rec[1]==username:
                pss=rec[2]
                hshkey = rec[3]
                check=True
                break
        if not check:
            print('Username not found.')
            sys.exit(0)
    
    elif len(result)==1:
        pss = result[0][2]
        hshkey = result[0][3]
    else:
        print('Site not found.')
        sys.exit(0)
        
    outputPassword(pss,hshkey)
try:
    DB.close()
except:
    pass
