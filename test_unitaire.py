import pytest
import sqlite3
import pickle
import numpy as np
import pandas as pd

conn=sqlite3.connect('db_test2.db')
c=conn.cursor()

f=c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,  admin INTEGER, username TEXT, password TEXT)')
if c==f:
    print('Table created!')
else:
    print('Table not created!')

assert c==f


username='Younglink'
password='K5644'
g=c.execute('INSERT INTO users(admin, username, password) VALUES (?,?,?)',(1,username,password))
if c==g:
    print('Table fulfilled!')
else:
    print('Not fulfilled!')

assert c==g


h=c.execute('SELECT * FROM users WHERE username =? AND password =?',(username, password))
if c==h:
    print('1')
else:
    print('0')
assert c==h


i=c.execute('SELECT * FROM users')
if c==i:
    print('Table displayed!')
else:
    print('Table not displayed!')
assert c==i


df=pd.read_csv('zirconia_cubic.csv')
df.head().to_sql("data", conn, if_exists="replace",index_label='id')

j=c.execute("select * from data")
if c==j:
    print('Data table created and displayed!')
else:
    print("Couldn't be created!")
assert c==j


k=c.execute('CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, username TEXT, predictions REAL)')
if c==k:
    print('Result table created')
else:
    print('Could not be created')
    
assert c==k