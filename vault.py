#Saint Leo University Summer 2 2020
#COM-430 Software Engineering

#Password Manager/Vault

#Project Lead/Algorithms by Hugh Ashley
#Release Manager/login flow by Eric Lawrence
#Tkinter GUI by Paul Cink

from tkinter import *
from tkinter import messagebox
#from PIL import ImageTK,Image
import sqlite3
import os
import hashlib
import datetime
import string
import secrets
from hashlib import sha256
root = Tk()

    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-----------------------Initilize-DB------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#Database
conn = sqlite3.connect('password_vault.db')
#Create cursor
c = conn.cursor()

#Create Tables if necessary

(c.execute("""CREATE TABLE IF NOT EXISTS vault (
id integer primary key,
username text,
account text,
hashval text,
updated date,
FOREIGN KEY(username) REFERENCES login(username)
)"""))
(c.execute("""CREATE TABLE IF NOT EXISTS login (
username text primary key,
password text
)"""))
(c.execute("""CREATE TABLE IF NOT EXISTS rainbow (
saltyHash text primary key,
password text
)"""))
#commit changes
conn.commit()
#close db
conn.close()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#----------------Login/Register screen----------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#Function to create root screen and populate it with login and register
#buttons upon application startup
def mainAccountScreen():
    global mainScreen
    mainScreen = Toplevel(root)
    mainScreen.title("Account Login")
    mainScreen.geometry("300x250")
    Label(text="").pack()
    Button(mainScreen, text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(mainScreen, text="Register", height="2", width="30", command=register).pack()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-----------------------Home Screen-------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#function to display home menu buttons after login
def buttons():
        user = activeUser
        Label(root, text="User: ", fg="green", font=("calibri", 11)).pack()
        Label(root, text=activeUser, fg="green", font=("calibri", 11)).pack()
    #Sign out button
        signout_btn = Button(root, text='Sign Out & Close',  width=15, command=root.destroy).pack()
    #Store Info Button
        genhash_btn = Button(root, text='Add Password', width=15, command=add).pack()
    #Show password Button
        showpass_btn = Button(root, text='Show Password', width=15, command=show).pack()
    




#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#---------------------Login Process------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#function to create login Screen and get entry from user
def login():


    global login_screen
    login_screen = Toplevel(root)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()


#Verify Login
def login_verify():

    if len(username_verify.get()) != 0:
        username1 = username_verify.get()
        password0 = password_verify.get()
    else:
        flag()
        
        
    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()    
    password1 = hashlib.sha224(str(password0).encode('utf-8')).hexdigest()
    
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    
    #Pull password hash from database
    validate = c.execute('SELECT password FROM login WHERE username = ?;', (username1,)).fetchone()
    check = validate [0]          
    #print(check)
    #print(password1)


    #compare using secrets method for security               
    if (secrets.compare_digest(check, password1) is True):
            setActiveUser(username1)
            login_success()
    else:
        flag()


    #Close Connection
    conn.close()    
    
#Notify user of login and passwords that need attention, display for 5 seconds
def login_success():
    global login_success_screen
    login_success_screen = Toplevel(root)
    login_success_screen.title("Success")
    login_screen.destroy()
    mainScreen.destroy()
    login_btn.destroy()
    buttons ()
    Label(login_success_screen, text="Login Success").pack()
    Label(login_success_screen, text="").pack()
    Label(login_success_screen, text="The Following Accounts\nHave Passwords Older\nThan 90 Days:").pack()
    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()
    #define test
    litmus = (datetime.date.today() - datetime.timedelta(90))
    #check db for pw older than 90 days
    check = c.execute("SELECT account FROM vault WHERE updated < ? ORDER BY account", (litmus,)).fetchall()
    #print accounts with pw older than 90 days
    for i in check:
        Label(login_success_screen, text=i).pack()
    #Close Connection
    conn.close()
    login_success_screen.after(5000,login_success_screen.destroy)
    

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#---------------------Registration Process-------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#Registration Screen
def register():
    global register_screen
    register_screen = Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, command = register_user).pack()
#Write to DB
def register_user():
    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()
    if len(username.get()) != 0:
        username_info = username.get()
    elif len(password.get()) != 0:
        password_info = password.get()
    else:
        flag()
    password_info = password.get()
    password_hash = hashlib.sha224(str(password_info).encode('utf-8')).hexdigest()
    c.execute('INSERT INTO login (username, password) VALUES (?, ?)', (username_info, password_hash))

    conn.commit()
    

    c.execute('Select * FROM login')

    #print(c.fetchall())
    
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

    #Close Connection
    conn.close()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-----------------Login/Registration Errors-------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#login errors
def flag():
    global flag
    flag = Toplevel(root)
    flag.title("Success")
    Label(flag, text="Invalid Username or Password").pack()
    Button(flag, text="Acknowledge", command=flag.destroy).pack()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#------------------------Active User--------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#set active user flag for db pulls and home screen
def setActiveUser(active_user):
    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()
    global activeUser
    
    activeUser = active_user

    

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-------------------Add Passwork to Vault---------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#add screen
def add():
    global addScreen
    addScreen = Toplevel(root)
    addScreen.title("Add Password")
    global passwd
    global acctname
    global passwd_entry
    global acctname_entry
    passwd = StringVar()
    acctname = StringVar()
    
    Label(addScreen, text="Password:").pack()
    passwd_entry = Entry(addScreen, width = 30, textvariable = passwd).pack()
    Label(addScreen, text="Account:").pack()
    acctname_entry = Entry(addScreen, width=30, textvariable = acctname).pack()
    Label(addScreen, text="").pack()
    Button(addScreen, text="Save", height="2", width="30", command = setPin).pack()
    Button(addScreen, text="Cancel", height="2", width="30", command = addScreen.destroy).pack()
    Label(addScreen, text="").pack()
#write to db
def saveacct(pin):    

    userPin=pin
    userPin=str(pin)
    runs=int(userPin)
    userPin = hashlib.sha224(str(userPin).encode('utf-8')).hexdigest()
    userPin = bytes(userPin, 'utf-8')
    username = activeUser
    userpass = passwd.get()
    username = activeUser
    account = acctname.get()
    global hashval
    hashval = hashlib.sha224(str(userpass).encode('utf-8')).hexdigest()
    hashcon = bytes(hashval, 'utf-8')
    updated = datetime.date.today()

    #print("written to db: ", username, account, hashval, updated)
    
    #Insert Into Table

    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()
    c.execute('INSERT INTO vault (username, account, hashval, updated) VALUES (?,?,?,?)',
              (username, account, hashcon, updated))
    
    #salt hash with pin and rehash
    salty = hashlib.pbkdf2_hmac('sha256', hashcon, userPin, runs).hex()
    #print("write salt: ", salty)
    #print("written to rainbow: ", salty)

    c.execute('INSERT INTO rainbow (saltyHash, password) VALUES (?,?)',
              (salty, userpass))
    
    #Commit changes
    conn.commit()    
    #Close Connection
    conn.close()



    
    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#----------------------Pin Handling------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#Get pin from user and pass to hash algorithm
def setPin():
    global setPinScreen
    setPinScreen = Toplevel(root)
    setPinScreen.title("Enter Pin")

    
    global setPin1
    global setPin_entry1
    setPin1 = StringVar()
    #setPin1.encode('utf-8')
    Label(setPinScreen, text="Please create a Pin,\n this will be used to"+
              "secure your\n passwords so do not forget it:").pack()
    setPin_entry = Entry(setPinScreen, width = 30, textvariable = setPin1, show = '*').pack()


    global setPin2
    global setPin_entry2
    setPin2 = StringVar()
    #setPin1.encode('utf-8')
    Label(setPinScreen, text="Please enter pin again: ").pack()
    setPin_entry = Entry(setPinScreen, width = 30, textvariable = setPin2, show = '*').pack()

    
    Button(setPinScreen, text = "Submit", command = checkPin ).pack()

#compare pins to make sure they match        
def checkPin():
    #hash pins for secure compare
    p1=setPin1.get()
    p2=setPin2.get()
    hp1=hashlib.sha224(str(p1).encode('utf-8')).hexdigest()
    hp2=hashlib.sha224(str(p2).encode('utf-8')).hexdigest()
    #print(hp1)
    #print(hp2)
    if (secrets.compare_digest(hp1, hp2) is True):
        saveacct(p1)
        addScreen.destroy()
        setPinScreen.destroy()
    else:
         Label(setPinScreen, text="Invalid Pin Entry").pack()

 
#prompt user for pin
def getPin(accountName):
    accountScreen.destroy()
    global getPinScreen
    getPinScreen = Toplevel(root)
    getPinScreen.title("Enter Pin for ")
    global getPin
    global getPin_entry
    #print(accountName)
    getPin = StringVar()
    Label(getPinScreen, text="Please enter the pin you\n used to store the password:").pack()
    getPin_entry = Entry(getPinScreen, width = 30, textvariable = getPin, show = '*').pack()
    Button(getPinScreen, text = "Submit", command = lambda: getPass(accountName) ).pack()

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#------------------------Pin Errors---------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#flag pins as not matching
def pinFlag():
    global pinFlag
    pinFlag = Toplevel(root)
    pinFlag.title("Success")
    Label(pinFlag, text="Invalid Pin Entry").pack()
    pinFlag.after(5000,login_success_screen.destroy)
    

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-----------------------Show Password----------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#dynamically display buttons   
def show():

    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()

    #Loop through results to populate a button for each account
    accounts = c.execute("SELECT account FROM vault WHERE username = ?", (activeUser,)).fetchall()
    global accountScreen
    accountScreen = Toplevel(root)
    accountScreen.title("Enter Pin")
    #currentAccount=accounts
    for i in accounts:
        #currentAccount=i
        Button(accountScreen, text = i, width = 20, command = lambda i=i:getPin(str(i))  ).pack()
     

    #Commit changes
    conn.commit()
    #Close Connection
    conn.close()
#Hash user input to derrive key for passwords
def getPass(acct):
    userPin1 =str(getPin.get())
    getPinScreen.destroy()
    userPin1 = str(userPin1)
    #print ("pin: ", userPin1)
    runs = int(userPin1)
    userPin1 = hashlib.sha224(str(userPin1).encode('utf-8')).hexdigest()
    userPin1 = bytes(userPin1, 'utf-8')
    #print ("hashed pin: ", userPin1)
    username = activeUser
    #print ("user:", username)
    account=str(acct)
    account = account.rstrip(",)'")
    account = account.lstrip("('")
    #print("account: ", account)
    #Database
    conn = sqlite3.connect('password_vault.db')
    #Create cursor
    c = conn.cursor()
    hval = c.execute("""SELECT DISTINCT hashval FROM vault WHERE username = ? AND account = ?""",
                     (username, account,)).fetchone()
    hvalue = str(hval[0])
    #print (hvalue)
    hval1 = hvalue.rstrip(",)")
    hval1 = hval1.lstrip("(")
    hval1 = hval1.lstrip("b'")
    hval1 = hval1.rstrip("'")
    hval1 = bytes(hval1, 'utf-8')
    #print ("read hashval: ", hval1)
    #To show the account password
    salt = hashlib.pbkdf2_hmac('sha256', hval1, userPin1, runs).hex()
    #print ("show pass salt: ",  salt)
    
    rainbows = c.execute('SELECT password FROM rainbow WHERE saltyHash = ?;', (salt,)).fetchone()

    #Commit changes
    conn.commit()
    #Close Connection
    conn.close()
    passout = rainbows[0]
    
    #print("password: ", passout)
    
    showpass(passout, account)
    
#display password to user in hilightable and copyable self destruct message
def showpass(passw, acct):
    global outPut
    outPut = Toplevel(root)
    outPut.title("password")
    pw=passw
    act=acct
    #print(pw)
    #print(act)
    p = StringVar()
    Label(outPut, text = "password for: ").pack()
    Label(outPut, text = act).pack()
    p.set(pw)    
    p = Entry(outPut, textvariable=p, state = "readonly").pack()
    Label(outPut, text = "Message will self destruct\nAfter 15 Seconds").pack()
    outPut.after(15000,root.destroy)

    
    


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-------------------------Driver--------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#Title
root.title('PW Manager')
#Window Size


login_btn = Button(root, text='ENTER THE VAULT', width=15, command = mainAccountScreen)
login_btn.pack()
    

root.mainloop()

