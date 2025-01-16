from cryptography.fernet import Fernet
import random
from random import shuffle
import hashlib
import os

def gen_ph():
	l = int(input("Input Password Length :: "))
	r = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	seed_list_nph = list(r.lower()) + list(r) + list("!@#$%^&*()_+") + list("1234567890")
	pass_nph = []
	for i in range(0,l):
		pass_nph.append(seed_list_nph[int(random.randint(0,len(seed_list_nph)-1))])
		shuffle(seed_list_nph)
	return(''.join(pass_nph))

def verify():
    try:
        f = open("id.txt","x")
        f.close()
        print("No user exists, lets create a new one !")
    except FileExistsError:
        print("User Exists !")
        
    with open("id.txt","r+") as credfile:
        creds = credfile.read()
        if os.path.getsize("id.txt") == 0:
            print("Please create a NEW User-ID and a strong memorable password to continue using this password manager for the first time:")
            print("Please not these is not recoverable later on process with caution")
            print("Don't worry these are hashed using SHA-256 so basically if your password is strong then it is impossible compromise them.")
            user = input("User ID :: ")
            pas = input("Password :: ")
            credfile.writelines(str(hashlib.sha256(user.encode()).hexdigest()))
            credfile.writelines(";")
            credfile.writelines(str(hashlib.sha256(pas.encode()).hexdigest()))
            credfile.writelines(";")
            key = Fernet.generate_key()
            credfile.writelines(str(key.decode()))
        else:
            usrin = input("Existing User ID : ")
            pasin = input("Password : ")
            r = creds.split(";")
            if (str(hashlib.sha256(usrin.encode()).hexdigest()) == r[0]) and (str(hashlib.sha256(pasin.encode()).hexdigest()) == r[1]):
                print("ACCESS GRANTED !")
            else:
                print("INVALID CREDENTIALS!")
                exit()

def store():
    try:
        f = open("creds.txt","x")
        f.close()
        print("No previous record of credentials found, Creating a new file")
    except FileExistsError:
        print("Credential File Exists !")
    with open("creds.txt","a") as addcred:
        sv = input("Name of Service :: ")
        usersv = input("Username :: ")
        passv  = input("Password :: ")
        gotkey = ((((open("id.txt","r")).read()).split(";"))[2])
        herekey = Fernet(gotkey)
        data = [sv,";",(herekey.encrypt(usersv.encode())).decode(),";",(herekey.encrypt(passv.encode())).decode()]
        addcred.writelines(data)

def retreive():
    try:
        f = open("creds.txt","x")
        f.close()
        print("No previous record of credentials found, Creating a new file")
    except FileExistsError:
        print("Credential File Exists !")
        
    with open("creds.txt","r") as retrievecred:
        svname = input("Service Name :: ")
        data = retrievecred.read()
        if svname in data:
            gotkey1 = ((((open("id.txt","r")).read()).split(";"))[2])
            herekey1 = Fernet(gotkey1)
            for i in range(0,len(data.split(";"))-1):
                if (data.split(";"))[i] == svname:
                    print("------ Record Found ! ------")
                    print("Service Name :: ", (data.split(";"))[i])
                    print("User :: ", (herekey1.decrypt((data.split(";"))[i+1])).decode())
                    print("Pass :: ", (herekey1.decrypt((data.split(";"))[i+2])).decode())
                    print("----------------------------")
                    exit()
                else:
                    print("No such record !")
                    exit()
        else:
            print("No such record!")

print("""
 /$$$$$$$                                                  /$$ /$$      /$$
| $$__  $$                                                | $$| $$$    /$$$
| $$  \ $$ /$$$$$$   /$$$$$$$ /$$$$$$$ /$$  /$$  /$$  /$$$$$$$| $$$$  /$$$$  /$$$$$$  /$$$$$$$
| $$$$$$$/|____  $$ /$$_____//$$_____/| $$ | $$ | $$ /$$__  $$| $$ $$/$$ $$ |____  $$| $$__  $$
| $$____/  /$$$$$$$|  $$$$$$|  $$$$$$ | $$ | $$ | $$| $$  | $$| $$  $$$| $$  /$$$$$$$| $$  \ $$
| $$      /$$__  $$ \____  $$\____  $$| $$ | $$ | $$| $$  | $$| $$\  $ | $$ /$$__  $$| $$  | $$
| $$     |  $$$$$$$ /$$$$$$$//$$$$$$$/|  $$$$$/$$$$/|  $$$$$$$| $$ \/  | $$|  $$$$$$$| $$  | $$
|__/      \_______/|_______/|_______/  \_____/\___/  \_______/|__/     |__/ \_______/|__/  |__/


Welcome to PasswdMan - intelligent password manager which can securely generate a password, store and retreive your 
credentails without a hassle and lesser problems as it is TOTALLY under YOUR control.

Available functionalities are :-

> Generate a strong password.
> Securly store all your credentials encrypted under the AES standard.
> Retrieve your credentials.
""")

verify()

task = (input("Please input a task to perform from the above :: ")).lower()

if task in "generate":
	print(gen_ph())
elif task in "store":
	store()
elif task in "retrieve":
	retreive()
