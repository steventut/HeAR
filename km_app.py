import streamlit as st
#from hugchat import hugchat
#from hugchat.login import Login
#import openai #9/22/2023  
import Login_Codes #9/3/2023
import knowledge_Database #9/22/2023

### Initialize Hugging Face Credentials
with st.sidebar:
    ##st.title('🤗💬 HugChat')
    st.title('企業智識庫機器人')
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

### MAIN CODES
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
#if session_state.knowledge_Database != 'Pizza Resturant':
if prompt := st.chat_input(disabled=not api_key):
#if prompt := st.chat_input(prompt): 
    if prompt != '':
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        knowledge_Database.collect_messages(prompt)

### 1. Select a demo knowledge Database
demo_knowledge_Database = st.sidebar.selectbox( 
    '1. Select a Knowledge Database (選擇知識庫)',
    ('None', 'Trading Strategy', 'Pizza Resturant', 'Class Reunion (preparing...)', '中醫客服機器人'))
## Launch chat using different knowledge Database, ### DO ONLY ONCE !!! initialize the demo knowledge Database
if demo_knowledge_Database == 'Pizza Resturant' and st.session_state.isLoadedPizzaResturant == False:
    session_state.knowledge_Database = 'Pizza Resturant'
    knowledge_Database.LoadPizzaResturant('')
    st.session_state.isLoadedPizzaResturant = True
    st.session_state.isLoadedTradingStrategy = False
    st.session_state.isLoadedChineseMedicine = False	
elif session_state.isLoggedIn and demo_knowledge_Database == 'Trading Strategy' and st.session_state.isLoadedTradingStrategy == False:
    session_state.knowledge_Database = 'Trading Strategy'
    knowledge_Database.LoadTradingStrategy('')
    st.session_state.isLoadedPizzaResturant = False
    st.session_state.isLoadedTradingStrategy = True 
    st.session_state.isLoadedChineseMedicine = False	
elif session_state.isLoggedIn and demo_knowledge_Database == 'Chinese Medicine' and st.session_state.isLoadedChineseMedicine == False:
    session_state.knowledge_Database = 'Chinese Medicine'
    knowledge_Database.LoadTChineseMedicine('')
    st.session_state.isLoadedPizzaResturant = False
    st.session_state.isLoadedTradingStrategy = False 
    st.session_state.isLoadedChineseMedicine = True 
elif demo_knowledge_Database != 'None':
   st.info("You need to login to access this function! Login or click SignUp in the left panel for free and get more autoML functionalities!")
	
### 2. Select a question to ask knowledge Database
if demo_knowledge_Database == 'None':
    question = st.sidebar.selectbox( 
    '2. Select a question to ask knowledge Database (發問)',('None'))
if demo_knowledge_Database == 'Trading Strategy':
    question = st.sidebar.selectbox( 
    '2. Select a question to ask knowledge Database (發問)',
    ('None', 'Can you create a new strategy based on these models?', 'List all models.', 'Create one more new model.', 'Ask your own question!'))
if demo_knowledge_Database == 'Pizza Resturant':
    question = st.sidebar.selectbox( 
    '2. Select a question to ask knowledge Database (發問)',
    ('None', 'I would like to order a pizza.', 'Pepperoni Large', 'no topping, but give me small coke!', 'List the detail of the order and total amount', 'Ask your own question!'))
if demo_knowledge_Database == '中醫客服機器人':
    question = st.sidebar.selectbox( 
    '2. Select a question to ask knowledge Database (發問)',
    ('None', '請問星期日有看診嗎', '請問陳國揚醫師星期一有沒有看診', '請問張維量醫師門診時間', 'Ask your own question!'))

# ask a question by Selecting a question to ask knowledge Database
if session_state.isLoggedIn and demo_knowledge_Database != 'None' and question != 'None' and question != 'Ask your own question!':
    knowledge_Database.collect_messages(question)

'''
# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    if 'isLoggedInChatBot' not in st.session_state:
	#st.session_state.isLoggedInChatBot = False
        # Hugging Face Login
        sign = Login(email, passwd)
        cookies = sign.login()
        # Create ChatBot                        
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        st.session_state.isLoggedInChatBot = chatbot
        ## Feature Request: Ability to select model #56
        # switch LLM,
        ##chatbot.switch_llm(0) # switch to OpenAssistant/oasst-sft-6-llama-30b-xor
        ##chatbot.switch_llm(1) # switch to meta-llama/Llama-2-70b-chat-hf
    #return chatbot.chat(prompt_input)
    ##try:
    response = st.session_state.isLoggedInChatBot.chat(prompt_input)
    return response
    ##except:
        ##return 'hugchat.exceptions.ChatError: Model is overloaded'

#DO ONLY ONCE !!! initialize the demo knowledge Database: Trading Strategy
if session_state.isLoggedIn and demo_knowledge_Database == 'Trading Strategy':
    #data3 = get_dataset(uploaded_file) #Steve: v1.9
    #data3 = session_state4.train_data
    #LSTM_codes.show_data(data3, classifier_name, params, session_state3.cwd)
    if 'isLoadedTradingStrategy' not in st.session_state:
        st.session_state.isLoadedTradingStrategy = True
        prompt = load_demo_knowledge_Database_trading_trategy()
        #st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                #st.write(prompt) #for debugging...
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
elif demo_knowledge_Database == 'Pizza Resturant':
   pass
elif demo_knowledge_Database != 'None':
   st.info("You need to login to access this function! Login or click SignUp in the left panel for free and get more autoML functionalities!")

# Generate a new response if last message is not from assistant
if session_state.knowledge_Database != 'Pizza Resturant':
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                st.write(prompt) #for debugging...
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

# ask a question...
if session_state.isLoggedIn and demo_knowledge_Database == 'Trading Strategy' and question != 'None' and question != 'Ask your own question!':
    #data3 = get_dataset(uploaded_file) #Steve: v1.9
    #data3 = session_state4.train_data
    #LSTM_codes.show_data(data3, classifier_name, params, session_state3.cwd)
    if 'isLoggedInChatBot' in st.session_state:
        prompt = question
        st.write(prompt)
        message = {"role": "user", "content": prompt}
        st.session_state.messages.append(message)	    
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                #st.write(prompt) #for debugging...
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
#elif question != 'None' or question != 'Ask your own question!':
#   st.info("You need to login to access this function! Login or click SignUp in the left panel for free and get more autoML functionalities!")
'''
