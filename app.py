import pytest
import logging
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from PIL import Image
import hashlib
import pickle
from pushover import Client


logging.basicConfig(level= logging.INFO, filename = "logging.log")


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def test_make_hashes():
    password='KING'
    assert len(password)>0

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False



conn=sqlite3.connect('db.db')
c=conn.cursor()

#df=pd.read_csv('zirconia_cubic.csv')
#df=df.drop(['Unnamed: 0','length'], 1)

img=Image.open('C:/Users/utilisateur/Desktop/Projet Final/Projet Officiel - Prédiction de prix de zicons/Round-Pure-Brilliance-sw-zirconia.jpg')
st.image(img,width=200)


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, admin INTEGER, username TEXT, password TEXT)')


def add_userdata(admin, username, password):
    c.execute('INSERT INTO users(admin, username, password) VALUES (?,?,?)',(admin, username, password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM users WHERE username =? AND password =?',(username, password))
    user=c.fetchall()
    return user

def view_all_users():
    c.execute('SELECT * FROM users')
    user = c.fetchall()
    return user


#df.to_sql("data", conn, if_exists="replace",index_label='id')


def view_all_data():
    c.execute("select * from data")
    data=c.fetchall()
    return data



def prediction(carat,cut,color,clarity,depth,table,width,height):
    pickle_in = open('model3.pkl', 'rb')
    regressor = pickle.load(pickle_in)
    predict_=[carat,cut,color,clarity,depth,table,width,height]
    price=np.array(predict_).reshape(-1,8)
    reg=regressor.predict(price)
    return reg

def test_prediction():
    pred1=prediction(1,2,3,4,5,6,7,8)
    pred2=prediction(2,4,6,8,10,12,14,16)
    pred3=prediction(4,5,7,8,70,70,10,8)
    assert pred1[0] > 5000
    assert pred2[0] > 10000
    assert pred3[0] < 20000


def create_resultstable():
    c.execute('CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, username TEXT, predictions REAL)')


def add_resultsdata(username, results):
    c.execute('INSERT INTO results(username, predictions) VALUES (?,?)',(username, results))
    conn.commit()

def view_all_results():
    c.execute('SELECT * FROM results')
    result = c.fetchall()
    return result



st.title('Zirconia Price Forecast')

menu = ['Home','Login','Sign Up','Signal a problem']
choice = st.sidebar.selectbox('Menu',menu)


if choice == 'Home':
    logging.info('Home menu')
    st.subheader('Home')
    
elif choice == "Login":
    logging.info('Login section')
    st.subheader('Login Section')

    username = st.sidebar.text_input('User Name')
    password = st.sidebar.text_input('Password',type='password')
    if st.sidebar.checkbox('Login'):
         #if password == '12345':
        create_usertable()
        hashed_pswd=make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        print(result)
        if result:
            logging.info('Logged as {}!'.format(username))
            st.success('Logged In as {}'.format(username))
            task = st.selectbox('Task',['Zirconia database','Predictions','User database'])
            if task == 'Zirconia database':
                st.subheader('Database')
                data_result = view_all_data()
                clean_db1 = pd.DataFrame(data_result,columns=['ID','Carat','Cut','Color','Clarity','Depth','Table','Width','Height','Price'])
                st.dataframe(clean_db1)

            elif task == 'Predictions':
                logging.info('Prediction page')
                st.subheader('Prediction')
                img1=Image.open('C:/Users/utilisateur/Desktop/Projet Final/Projet Officiel - Prédiction de prix de zicons/c0014142-800px-wm.jpg')
                st.image(img1,width=100)
                carat= st.number_input('Carat')
                cut=st.selectbox('Cut',range(1,6))
                color=st.selectbox('Color',range(1,10))
                clarity=st.selectbox('Clarity',range(1,9))
                depth= st.number_input('Depth')
                table=st.number_input('Table')
                width=st.number_input('Width')
                height=st.number_input('Height')
                pred=prediction(carat,cut,color,clarity,depth,table,width,height)
                logging.info('Prediction made')
                st.write('The potential zirconia cubic price should be : ${}'.format(pred[0]))
                create_resultstable()
                add_resultsdata(username, pred[0])
                res = pd.DataFrame(view_all_results(),columns=['ID','Username','Prediction'])
                st.dataframe(res)

            elif task == 'User database':
                logging.info('Users database')
                st.subheader('User database')
                user_result = view_all_users()
                clean_db2 = pd.DataFrame(user_result,columns=['ID','Admin','Username','Password'])
                st.dataframe(clean_db2)
                
        else:
            logging.error('Incorrect Username or Password!')
            st.warning('Incorrect Username/Password')

elif choice == 'Sign Up':
    logging.info('Sign Up page')
    autorisation=st.selectbox("Are you administrator?",["Yes","No"],index=1)
    if autorisation=="Yes":
        logging.info('Please enter password')
        st.info("Please enter administrator password")
        password = st.text_input("Password",type='password')
        if password!="YoungLink93@*":
            logging.error('Incorrect password!')
            st.error("Administrator password incorrect!")
    
        elif password=="YoungLink93@*":
            logging.warning("Please enter your ids!")
            st.info("Please enter your ids")
            username = st.text_input("username")
            password3 = st.text_input("Password",type='password',key=2)
            password4 = st.text_input("Please confirm your password",type='password',key=3)
            if st.button("Sign up") and password3==password4:
                logging.info('Informations displayed')
                st.write(""" Here are your informations :
                user : {}
                password : {}""".format(username,make_hashes(password4)))
                admin=1
                st.write("You are the administrator! Code {}".format(admin))
                create_usertable()
                add_userdata(admin, username, make_hashes(password4))
                logging.info('Account created!')
                st.success('You have successfully created a valid account!')
                st.info('Go to to Login menu to login')
            elif password3!=password4:
                logging.error('Incorrect matching!')
                st.error("Passwords do not match each other !")
    else:
        logging.warning("Please enter your ids!")
        st.info("Please enter your ids")
        username = st.text_input("username",key=4)
        password3 = st.text_input("Password",type='password',key=5)
        password4 = st.text_input("Please confirm your password",type='password',key=6)
        if st.button("Sign up",key=7) and password3==password4:
            logging.info('Informations displayed')
            st.write(""" Here are your informations :
            user : {}
            password : {}""".format(username,make_hashes(password4)))
            admin=0
            st.write("You are not the administrator: Code {}".format(admin))
            create_usertable()
            add_userdata(admin, username, make_hashes(password4))
            logging.info('Account created!')
            st.success('You have successfully created a valid account!')
            st.info('Go to to Login menu to login')
        elif password3!=password4:
            logging.error('Incorrect matching!')
            st.error("Passwords do not match each other !")
       
elif choice == 'Signal a problem':
    logging.info('Problem signaled!')
    client = Client("utyoawn8mwpzacm4v6ksmuk6qqdjaz", api_token="askzvf52zwwmypoh1kyzj7xgynjt9i")
    client.send_message("Hello! If you have met a problem, send a text message to 0785121093!", title="Hello")
    st.success('We have sent you a message!')