import getpass
from io import StringIO
import logging
import random
import time
import colorama
from colorama import Fore, Back, Style
from tqdm import tqdm
from WSS import User, db, get_hashed_password

db.create_all()
print("Database installed successfully!")
colorama.init()

username = input("Enter a Username for WKit; ")
passwd = get_hashed_password(getpass.getpass("Enter a Password for this User").strip("\r\t\n").encode()).decode()
user = User(username=username.strip("\r\t\n"), password=passwd)
db.session.add(user)
db.session.commit()
print("Initialized WKit!")
