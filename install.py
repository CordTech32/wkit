import getpass
from io import StringIO
import logging
import random
import time
import colorama
from colorama import Fore, Back, Style
from tqdm import tqdm
from sqlite3 import connect
from WSS import get_hashed_password

db = connect("users.db")
db.execute("CREATE TABLE user(id integer primary key autoincrement, username text unique default 'Wk-Admin', password text not null)")
db.execute("CREATE TABLE html(id integer primary key autoincrement, rule text unique default '/', html text not null, render_type text not null)")
print("Database installed successfully!")
colorama.init()

username = input("Enter a Username for WKit; ")
passwd = get_hashed_password(getpass.getpass("Enter a Password for this User").strip("\r\t\n").encode()).decode()
c = db.cursor()
new_i = 1+len(c.execute("SELECT * FROM user").fetchall())
db.execute("INSERT INTO user VALUES(?, ?,?)", (new_i, username, passwd))
db.commit()
db.close()
print("Initialized WKit!")
