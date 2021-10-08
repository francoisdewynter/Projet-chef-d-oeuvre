import logging
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from PIL import Image
import hashlib
import pickle

logging.basicConfig(level= logging.INFO, filename = "logging.log")


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

conn=sqlite3.connect('database.db')
c=conn.cursor()

#df=pd.read_csv('zirconia_cubic.csv')
#df=df.drop(['Unnamed: 0','length'], 1)

img=Image.open('C:/Users/utilisateur/Desktop/Projet Final/Projet Officiel - Prédiction de prix de zicons/static/Round-Pure-Brilliance-sw-zirconia.jpg')
st.image(img,width=200)


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO users(username, password) VALUES (?,?)',(username, password))
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


def create_resultstable():
    c.execute('CREATE TABLE IF NOT EXISTS results(id INTEGER PRIMARY KEY, username TEXT, predictions REAL)')


def add_resultsdata(username, results):
    c.execute('INSERT INTO results(username, predictions) VALUES (?,?)',(username, results))
    conn.commit()


def view_all_results():
    c.execute('SELECT * FROM results')
    result = c.fetchall()
    return result


def main():

    st.title('Zirconia Price Forecast')

    menu = ['Home','Login','Sign Up']
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
                    clean_db2 = pd.DataFrame(user_result,columns=['ID','Username','Password'])
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
                admin,user=1,0
                if st.button("Save data and sign up!") and password3==password4:
                    logging.info('Informations displayed')
                    st.write(""" Here are your informations :
                    user : {}
                    password : {}""".format(username,make_hashes(password4)))
                    st.write("Admin : {}, User : {}".format(admin,user))
                    create_usertable()
                    add_userdata(username, make_hashes(password4))
                    logging.info('Account created!')
                    st.success('You have successfully created a valid account!')
                    st.info('Go to to Login menu to login')
                elif password3!=password4:
                    logging.error('Incorrect matching!')
                    st.error("Passwords do not match each other !")
                elif autorisation=="Non":
                    logging.warning('Please enter your ids!')
                    st.info("Please enter ids")
                    username = st.text_input("User")
                    password3= st.text_input("Password",type='password',key=4)
                    password4 = st.text_input("Please confirm password",type='password',key=5)
                    admin,user=0,1
                    if st.button("Save your data !") and password3==password4:
                        logging.info('Informations saved!')
                        st.write(""" Here are the informations :
                        user : {}
                        password : {}""".format(username,password4))
                        st.write("Admin : {}, User : {}".format(admin,user))
                    elif password3!=password4:
                        logging.error('Incorrect password matching!')
                        st.error("Passwords do not correspond each other !")   
                #st.subheader('Retype your idents to create a new account')
                #new_user = st.text_input('Username')
                #new_password = st.text_input('Password', type='password',key=6)
                    

if __name__ == '__main__':
	main()