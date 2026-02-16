### Revision history
## version 1.0 Initial development for google/HeAR app for PD progression Monitoring

import streamlit as st
#from hugchat import hugchat
#from hugchat.login import Login
#import openai #9/22/2023  
import Login_Codes #9/3/2023
import knowledge_Database #9/22/2023
import time
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean
from datetime import datetime
import matplotlib.pyplot as plt

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

    # Demo 1: show baseline model (no new patient)
    # --- 5. GENERATE PLOT 1: UPDATED PCA MAP ---
    all_vectors = [golden_vector] + healthy_vectors + pd_vectors
    #all_vectors = [golden_vector] + healthy_vectors + pd_vectors + new_vecs
    pca = PCA(n_components=2)
    all_2d = pca.fit_transform(np.array(all_vectors))

    gold_2d = all_2d[0]
    healthy_2d = all_2d[1:len(healthy_vectors)+1]
    #pd_2d = all_2d[len(healthy_vectors)+1:-1]
    pd_2d = all_2d[1+len(healthy_vectors)+1:1+len(healthy_vectors)+1+len(pd_vectors)]
    new_2d = []
    #new_2d = all_2d[-len(new_vecs):]

    ### Copy codes from Main Program: Progression Monitoring Dashboard (1)
    # Cell 11: Main Program: Progression Monitoring Dashboard (1): PCA Clustering Map
    ## Steve: cut it here! The following codes are for plotting Cluster Map!!
    plt.figure(figsize=(16, 10)) # Made figure slightly larger for labels

    # 1. Background Clusters
    plt.scatter(healthy_2d[:, 0], healthy_2d[:, 1], c='green', alpha=0.7, s=150, edgecolors='darkgreen', label='Healthy Ref')
    plt.scatter(pd_2d[:, 0], pd_2d[:, 1], c='red', alpha=0.8, s=150, edgecolors='darkred', label='PD History')

    # 3. Golden Vector
    plt.scatter(gold_2d[0], gold_2d[1], c='gold', s=700, marker='*', edgecolors='black', linewidth=1.5, zorder=15, label='Target (Golden Vector)')

    # 4. RED ARROWS (PD History -> Gold) (UPDATED)
    # Using `arrowprops` to draw red arrows pointing to the star
    for pt in pd_2d:
        plt.annotate("",
                 xy=(gold_2d[0], gold_2d[1]), xycoords='data', # Head of arrow (Target)
                 xytext=(pt[0], pt[1]), textcoords='data',     # Tail of arrow (Source)
                 arrowprops=dict(arrowstyle="->", color='red', linestyle='--', linewidth=1.5, alpha=0.5))

    # 5. The New Person (Blue Dot)
    if len(new_2d) != 0:
        plt.scatter(new_2d[:,0], new_2d[:,1], c='blue', s=400, edgecolors='white', linewidth=3, zorder=20, label='New Input')
        for i, txt in enumerate(new_labels):
            plt.annotate(txt, (new_2d[i, 0], new_2d[i, 1]),
                 xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7, color='darkgreen')

    plt.title("Voice Biomarker Map: Patient Assessment", fontsize=16, weight='bold')
    plt.xlabel("Principal Component 1 (Vocal Variance)", fontsize=12)
    plt.ylabel("Principal Component 2 (Tone Quality)", fontsize=12)
    plt.legend(loc='lower right', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    st.pyplot()

    ### Main Program: Progression Monitoring Dashboard (2)
    # Cell 12: Main Program: Progression Monitoring Dashboard (2): 
    # 4 plots in one graph: AI distance, Jitter, Shimmer, moor_UPDRS score
    ##from IPython.display import display

    # 1. Combine all variables into a single dictionary, then create a DataFrame
    ##data = {
    ##    'Label': new_labels,
    ##    'Distance from Golden Vector': new_distances,
    ##    'Jitter': new_jitters,
    ##    'Shimmer': new_shimmers,
    ##    'Predicted motor_UPDRS': new_updrs_scores
    ##}
    ##df_new = pd.DataFrame(data)

    # Load the data back from the CSV file into a new variable
    df_sorted = pd.read_csv("data_for_4_plots.csv")
    ##df_sorted = pd.concat([df_sorted, df_new], ignore_index=True)
    ##print(df_sorted)

    ##print("Successfully loaded 'data_for_4_plots.csv' into df_sorted_back:")
    ## Display the first few rows to verify it loaded correctly
    ##display(df_sorted)

    # 3. Merge all 4 plots into one single plot
    plt.figure(figsize=(14, 8))

    # Plot each trend on the same axis
    plt.plot(df_sorted.index, df_sorted['Distance from Golden Vector'], label='Distance (Overall Recovery)', marker='o', linewidth=2)
    plt.plot(df_sorted.index, df_sorted['Jitter'], label='Frequency Instability (Jitter)', marker='s', linewidth=2)
    plt.plot(df_sorted.index, df_sorted['Shimmer'], label='Amplitude Instability (Shimmer)', marker='^', linewidth=2)
    plt.plot(df_sorted.index, df_sorted['Predicted motor_UPDRS'], label='Predicted motor_UPDRS', marker='x', linewidth=2)

    # Add the two requested dashed horizontal lines
    plt.axhline(y=30, color='blue', linestyle='--', linewidth=2, label='Healthy Acceptance Level')
    plt.axhline(y=15, color='brown', linestyle='--', linewidth=2, label='Mild Threshold (<15)')

    # Formatting the plot
    plt.title('Combined Trends for HeAR Evaluation (Sorted by Distance)', fontsize=16)
    plt.xlabel('Patient/Sample Labels', fontsize=12)
    plt.ylabel('Feature Values', fontsize=12)

    # Set the x-ticks to be the actual labels from your data
    plt.xticks(ticks=df_sorted.index, labels=df_sorted['Label'], rotation=45, ha='right')

    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=12, loc='best')
    plt.tight_layout()

    # Show the merged plot
    plt.show()
    st.pyplot()

    ### 
    # Cell 13: Main Program: Progression Monitoring Dashboard (3): 
    # 3 plots: AI distance, Jitter, Shimmer
    ## fig, axes = plt.subplots(2, 1, figsize=(14, 20))
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # --- Plot 1: Distance from Golden Vector ---
    axes[0].plot(df_sorted.index, df_sorted['Distance from Golden Vector'], marker='o', color='blue', linewidth=2)
    axes[0].set_title('Overall Recovery: Distance from Golden Vector (google/HeAR)', fontsize=14)
    axes[0].set_ylabel('Distance')
    axes[0].axhline(y=30, color='green', linestyle='--', linewidth=2, label='Healthy Threshold')
    axes[0].legend(loc='center')

    # --- Plot 2: Frequency Instability (Jitter) ---
    axes[1].plot(df_sorted.index, df_sorted['Jitter'], marker='s', color='orange', linewidth=2)
    axes[1].set_title('Frequency Instability (Jitter)', fontsize=14)
    axes[1].set_ylabel('Jitter')
    axes[1].axhline(y=0.8, color='green', linestyle='--', linewidth=2, label='Healthy Threshold')
    axes[1].legend(loc='center')

    # --- Plot 3: Amplitude Instability (Shimmer) ---
    axes[2].plot(df_sorted.index, df_sorted['Shimmer'], marker='^', color='green', linewidth=2)
    axes[2].set_title('Amplitude Instability (Shimmer)', fontsize=14)
    axes[2].set_ylabel('Shimmer')
    axes[2].axhline(y=3, color='green', linestyle='--', linewidth=2, label='Healthy Threshold')
    axes[2].legend(loc='center')

    # --- Plot 4: Predicted motor_UPDRS ---
    ##axes[3].plot(df_sorted.index, df_sorted['Predicted motor_UPDRS'], marker='x', color='red', linewidth=2)
    ##axes[3].set_title('Predicted motor_UPDRS', fontsize=14)
    ##axes[3].set_ylabel('UPDRS Score')
    ##axes[3].set_xlabel('Patient/Sample Labels', fontsize=14)

    # Apply unified formatting to all 4 subplots
    axes[0].grid(True, linestyle='--', alpha=0.7)
    axes[1].grid(True, linestyle='--', alpha=0.7)
    axes[2].grid(True, linestyle='--', alpha=0.7)
    # Ensure X-axis shows the sorted labels properly
    axes[0].set_xticks(ticks=df_sorted.index)
    axes[1].set_xticks(ticks=df_sorted.index)
    axes[2].set_xticklabels(labels='', rotation=45, ha='right')
    axes[2].set_xticks(ticks=df_sorted.index)
    axes[2].set_xticklabels(labels=df_sorted['Label'], rotation=45, ha='right')

    # Adjust layout to prevent overlapping labels and titles
    plt.tight_layout()

    # Render the 3 distinct plots
    plt.show()
    st.pyplot()

menu_functions = ["Product Description", "Baseline Model","Ahh: Voice Biomarker", "Monitoring History"]
choice_menu = st.sidebar.radio("Menu", menu_functions)
if choice_menu == "Product Description":
    st.title("Prodcut Description")
    st.markdown("### Parkinson Disease Progression Monitoring System using Voice Biomarker（google/HeAR）")
elif choice_menu == "Baseline Model":
    st.title("Baseline Model")
    st.markdown("### Clustering Voice Biomarker for both Healthy People and Parkinson Patients")
    load_data()
