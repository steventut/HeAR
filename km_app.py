import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import Login_Codes #9/3/2023
import Pizza_Resturant #9/22/2023

### Initialize Hugging Face Credentials
with st.sidebar:
    ##st.title('🤗💬 HugChat')
    st.title('企業智識庫機器人')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        ##st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
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
session_state4 = st.session_state	
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
    session_state4.train_data = ''
    ##rerun() #9/13/2023
    #st.stop()
    st.experimental_rerun()
    demo_knowledge_Database = 'None'
    session_state.knowledge_Database = ''
#else:
#    st.sidebar.text_input("Logged in as", session_state2.logged_in_name)
#    st.write("Logged in as", session_state2.logged_in_name)
#v1.6 login: end!    

### select demo KM database
def load_demo_knowledge_Database_trading_trategy():
    prompt = '''The following models are trading strategies categorized as Examples-1-Models.

Model 1:
HYPOTHESIS: If a company efficiently uses its assets (equipment, patents etc.) to generate
sales, its stock may outperform the stock of its peers in the future. Denoted by the asset
turnover ratio : sales/assets
IMPLEMENTATION: If company A's asset turnover ratio is better than company B's, stock A
may outperform stock B. However, directly using the input (sales/assets) may put unusually
large long positions (buy) or short positions (sell) on outlier stocks. Rank operator removes
the vast variation of input values by ranking the input and returning float numbers equally
distributed between 0 and 1.
IMPROVEMENT: Find and simulate more fundamental ratios that are factors in determining
a company's performance and financial health.
Datafields: sales, assets
Operators: rank
Expression:
rank(sales / assets)

Model 2:
HYPOTHESIS: If the stock price of a company has increased over the last 2 days, it may
decrease in the future (time series delta of closing price today and closing price 2 days ago).
IMPLEMENTATION: If company A's stock price had increased twice as much as the stock
price of another company B, the prices of both stocks may decrease in the future. In this
reversion example, stock A may not fall double stock B, though it may fall more than stock B
(rank operator).
IMPROVEMENT: Can different neutralizations and decay settings improve this signal?
Under what neutralization would a reversion idea work best?
Datafields: close
Operators: rank, ts_delta
Expression:
rank(-ts_delta(close, 2))

Model 3:
HYPOTHESIS: If today's stock price is higher than the geometric mean price of the week
[time series product of price over 5 days raised to power (1/5)], then the stock price may fall
in the future.
IMPLEMENTATION: Directly using the input (close-ts_product(close,5)^0.2) may put
unusually large long positions (buy) or short positions (sell) on outlier stocks. Rank operator
removes the vast variation of input values by ranking the input and returning float numbers
equally distributed between 0 and 1.
IMPROVEMENT: How do you handle outlier values? Under what neutralization would a
reversion idea work best?
Datafields: close
Operators: ts_product
Expression:
ts_product(close, 5) ^ 0.2 - close'''
    return prompt

### MAIN CODES
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

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

# User-provided prompt
#if session_state.knowledge_Database != 'Pizza Resturant':
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
#if prompt := st.chat_input(prompt): 
    if prompt != '':
        st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if session_state.knowledge_Database == 'Pizza Resturant' and st.session_state.isLoadedPizzaResturant == True:
    Pizza_Resturant.collect_messages(prompt)

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

### 1. Select a demo knowledge Database
demo_knowledge_Database = st.sidebar.selectbox( 
    '1. Select a demo knowledge Database',
    ('None', 'Trading Strategy', 'Pizza Resturant', 'Class Reunion (preparing...)'))
## Launch chat using different knowledge Database
#if session_state.isLoggedIn and demo_knowledge_Database == 'Trading Strategy':
if demo_knowledge_Database == 'Pizza Resturant' and st.session_state.isLoadedPizzaResturant == False:
    session_state.knowledge_Database = 'Pizza Resturant'
    Pizza_Resturant.main_function('')
    st.session_state.isLoadedPizzaResturant = True
    
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

### 2. Select a question to ask knowledge Database
question = st.sidebar.selectbox( 
    '2. Select a question to ask knowledge Database',
    ('None', 'Can you create a new strategy based on these models?', 'List all models.', 'Create one more new model.', 'Ask your own question!'))
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
