import streamlit as st 
import pandas as pd
#Login (https://blog.jcharistech.com/2020/05/30/how-to-add-a-login-section-to-streamlit-blog-app/)
import os
import base64

#https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/27
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
#global filename
#filename = 'finalized_model_Cluster_KMeans.sav'  

#os.system('chmod +w userdata.db')

def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None)) 
    
#Login
def Login(session_state, session_state2, session_state3):
    st.subheader("Login Section")
    username = st.text_input("User Namee (your email)", value='')
    password = st.text_input("Password",type='password', value='')
    st.write("Don't have an account? Click SignUp in the left panel for free and  get more autoML functionalities!")
    if st.button("Login"):
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        if result:
            #st.success("Logged In as {}".format(username))
            #Set state variable here:
            session_state2.logged_in_name = username
            session_state.isLoggedIn = True
            #rerun()      
            #v1.7: create and change directory
            #星翰 changed the codes:
            #cwd = os.getcwd() + '/automlweb/v1.9/AccountLists/' + session_state2.logged_in_name
            #Steve: changed it back! 8/10/2021, need to commit again!
            cwd = os.getcwd() + '/' + session_state2.logged_in_name
            if not (os.path.isdir(cwd)):
                os.mkdir(cwd)
            session_state3.cwd = cwd
            #os.chdir(cwd) #chdir will make big trouble!!!
            st.write("Current working directory:",cwd)
            #st.info("Current working directory:",cwd)
            st.success("Current working directory:{0}".format(cwd))
            
            if username == 'ntut@ntut.com' and password == 'automl1':
                st.subheader("User Profiles")
                user_result = view_all_users()
                #clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                clean_db = pd.DataFrame(user_result)
                st.dataframe(clean_db)
                st.markdown(get_binary_file_downloader_html('userdata.db', 'db'), unsafe_allow_html=True)
                return #if I rerun(), I can't see the User Profiles!!!
            ##rerun() #Steve: 02-11-2021, 9/13/2023 => crashed!
            #st.stop()
            st.experimental_rerun()
        else:
            st.warning("Incorrect Username/Password")

#SignUp
def SignUp():
    st.subheader("Create New Account")
    new_user = st.text_input("Username (your email)", value='')
    new_password = st.text_input("Password",type='password', value='')
    #v1.7: add more user info
    new_FirstLastName = st.text_input("First and Last Name", value='')
    new_CompanyInstitutionName = st.text_input("Company/Institution Name", value='')    
    new_Country = st.text_input("Country (1:Asia 2:Africa 3:North America 4:South America 5:Antarctica 6:Europe 7:Australia)", value='')    
    new_PrimaryInterest = st.text_input("Primary Interest (1:Teacher 2:Student 3:Industrial Practitioner)", value='')    
    
    if st.button("Signup"):
        #if new_user.find('@') == -1: #Steve: comment out temparary!
        #    st.warning("Username must have email's format!")
        #    return
        if new_user == '' or new_user == ' ' or new_password == '' or new_password == ' ':
            st.warning("Incorrect Username/Password")
            return           
        create_usertable()
        add_userdata(new_user,make_hashes(new_password),new_FirstLastName,new_CompanyInstitutionName,new_Country,new_PrimaryInterest)
        st.success("You have successfully created a valid Account")
        st.info("Click Login Radio Button in the left panel to login!")       
            
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('userdata.db', check_same_thread=False) #v1.9,Steve added!
c = conn.cursor()

# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT, FirstLastName TEXT,CompanyInstitutionName TEXT,Country TEXT,PrimaryInterest TEXT)')

def add_userdata(username,password,FirstLastName,CompanyInstitutionName,Country,PrimaryInterest):
    c.execute('INSERT INTO userstable(username,password,FirstLastName,CompanyInstitutionName,Country,PrimaryInterest) VALUES (?,?,?,?,?,?)',(username,password,FirstLastName,CompanyInstitutionName,Country,PrimaryInterest))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
