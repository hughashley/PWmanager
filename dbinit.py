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
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
#-----------------------Initilize-DB------------------------#
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#
class DB:
	#Create Tables if necessary
	def __init__(self):
		#Database
		conn = sqlite3.connect('password_vault.db')
		#Create cursor
		c = conn.cursor()
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
