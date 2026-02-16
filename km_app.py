### Revision history
## version 1.0 Initial development for google/HeAR app for PD progression Monitoring

import streamlit as st
#from hugchat import hugchat
#from hugchat.login import Login
#import openai #9/22/2023  
import Login_Codes #9/3/2023
import knowledge_Database #9/22/2023
import time

### Initialize Hugging Face Credentials
with st.sidebar:
    ##st.title('🤗💬 HugChat')
    st.title('Parkinson Disease Progression Monitoring using Voice Biomarker')
    st.write('v1.0')
    #if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
    if 'api' in st.secrets:
        ##st.success('HuggingFace Login credentials already provided!', icon='✅')
        #hf_email = st.secrets['EMAIL']
        #hf_pass = st.secrets['PASS']
	#openai.api_key = st.secrets['api']
        api_key = True
    else:
        #hf_email = st.text_input('Enter E-mail:', type='password')
        #hf_pass = st.text_input('Enter password:', type='password')
        api_key = st.text_input('Enter api_key:', type='password')
        #if not (hf_email and hf_pass):
        if not api_key:
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    ##st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')
    
# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "企業智識庫機器人在此提供諮詢服務，How may I help you?"}]
if "messages2" not in st.session_state.keys():
    st.session_state.messages2 = []

### initialize login 
def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))   
session_state = st.session_state
session_state2 = st.session_state
session_state3 = st.session_state
#session_state4 = st.session_state	
if 'isLoggedIn' not in st.session_state:
	st.session_state.isLoggedIn = False	
	session_state.knowledge_Database = ''
	demo_knowledge_Database = 'None'
	question = 'None'
#session_state2 = SessionState.get(logged_in_name='')
if 'logged_in_name' not in st.session_state:
	st.session_state.logged_in_name = ''	
#session_state3 = SessionState.get(cwd='')
if 'cwd' not in st.session_state:
	st.session_state.cwd = ''	
if 'isLoadedPizzaResturant' not in st.session_state:
    st.session_state.isLoadedPizzaResturant = False
if 'isLoadedTradingStrategy' not in st.session_state:
    st.session_state.isLoadedTradingStrategy = False
if 'isLoadedChineseMedicine' not in st.session_state:
    st.session_state.isLoadedChineseMedicine = False
if 'isLoadedTA' not in st.session_state:
    st.session_state.isLoadedTA = False
if 'isLoadedPCBA' not in st.session_state:
    st.session_state.isLoadedPCBA = False
if 'isLoadedAIagent' not in st.session_state:
    st.session_state.isLoadedAIagent = False

if 'isOpenAiAPIError' not in st.session_state:
    st.session_state.isOpenAiAPIError = False
if 'isOpenAiAPIErrorEver' not in st.session_state:
    st.session_state.isOpenAiAPIErrorEver = False	
	
menu = ["None: try it out without login","SignUp: for free","Login: for more functionalities"]
if session_state.isLoggedIn:
    #st.sidebar.text_input("Logged in as", session_state2.logged_in_name)
    #st.write("Logged in as", session_state2.logged_in_name)
    #st.write("Current working directory:", session_state3.cwd)
	
    menu = ["Logged in as " + session_state2.logged_in_name, "Logout"]
    #choice = st.sidebar.radio("Login or SignUp for free",menu)
    #if choice == "Logout":
    #    session_state.isLoggedIn = False
    #    session_state2.logged_in_name = ''
    #    session_state3.cwd = ''
    #    session_state4.train_data = ''
    #    rerun()
    #menu = ["None: try it out without login","SignUp: for free","Login: for more functionalities"]
    #v1.7: create and change directory
    #cwd = os.getcwd() + '/' + session_state2.logged_in_name
    #if not (os.path.isdir(cwd)):
    #    os.mkdir(cwd)
    #os.chdir(cwd)
    #st.write("Current working directory:",cwd)
    #st.sidebar.radio("Login or SignUp for free",index=0)
#if session_state.isLoggedIn == False:
#    menu = ["None: try it out without login","SignUp: for free","Login: for more functionalities"]
choice = st.sidebar.radio("Login or SignUp for free",menu)
if choice == "Login: for more functionalities":
    Login_Codes.Login(session_state, session_state2, session_state3)
    #Login_Codes_Firebase.Login_Firebase(session_state, session_state2, session_state3) #SOS
    #pass
    #choice = "None: try it out without login"
##elif choice == "SignUp: for free":    
    ##Login_Codes.SignUp()  #9/13/2023 disable signup
    #Login_Codes_Firebase.SignUp_Firebase()   #SOS
    #pass
elif choice == "Logout":
    session_state.isLoggedIn = False
    session_state2.logged_in_name = ''
    session_state3.cwd = ''
    #session_state4.train_data = ''
    ##rerun() #9/13/2023
    #st.stop()
    st.experimental_rerun()
    demo_knowledge_Database = 'None'
    session_state.knowledge_Database = ''
    st.session_state.isLoadedPizzaResturant = False
    st.session_state.isLoadedTradingStrategy = False
    st.session_state.isLoadedChineseMedicine = False	
    st.session_state.isLoadedAIagent = False

##### HeAR added!
st.set_page_config(
    page_title="Parkinson Disease Progression Monitoring System",
    #page_icon="🐕",
    layout="wide"
)
### Load voice files to generate embedding vectors and calculate AI distance
def load_data():
    healthy_vectors_back = pd.read_csv("healthy_vectors.csv")
    healthy_vectors = healthy_vectors_back.values.tolist()
    golden_vector = np.mean(healthy_vectors, axis=0)
    avg_healthy_dist = np.mean([euclidean(v, golden_vector) for v in healthy_vectors])

    pd_vectors_back = pd.read_csv("pd_vectors.csv")
    pd_vectors = pd_vectors_back.values.tolist()

menu_functions = ["Product Description", "Baseline Model","Ahh: Voice Biomarker", "Monitoring History"]
choice_menu = st.sidebar.radio("Menu", menu_functions)
if choice_menu == "Product Description":
    st.title("Prodcut Description")
    st.markdown("### Parkinson Disease Progression Monitoring System using Voice Biomarker（google/HeAR）")
elif choice_menu == "Baseline Model":
    st.title("Baseline Model")
    st.markdown("### Clustering Voice Biomarker for both Healthy People and Parkinson Patients")
	load_data()
