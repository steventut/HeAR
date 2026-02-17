# Demo 2: I will simulate a new pd patient, talk to cell phone with shaky voice
import streamlit as st
from scipy.spatial.distance import euclidean
from datetime import datetime

session_new = st.session_state  #keep new patients' 6 info
if 'new_vecs' not in session_new:
  session_new.demo_stage = "Baseline Model"
  session_new.new_vecs = []
  session_new.new_labels = []
  session_new.new_distances = []
  session_new.new_jitters = []
  session_new.new_shimmers = []
  session_new.new_updrs_scores = []

@st.cache_resource
def Login_huggingface_and_Load_HeAR_model():
  #Cell 2: Login to Huggin Face
  from huggingface_hub.utils import HfFolder
  
  if HfFolder.get_token() is None:
      from huggingface_hub import notebook_login
      notebook_login()
  # Cell 5: Load google/HeAR Model
  from huggingface_hub import from_pretrained_keras
  
  # Load the model directly from Hugging Face Hub
  loaded_model = from_pretrained_keras("google/hear")
  st.write("✅ AI Ready.")
  return loaded_model

def new_patients():
  # --- 4. PROCESS NEW PERSON ---
  session_new.demo_stage = "Ahh: Capturing Voice Biomarker" #New patient comeing in for healthy and PD progression check
  Login_huggingface_and_Load_HeAR_model()
  st.write (f"--- 🔍 Analyzing New Input: new_person_file ---")
  new_person_file = "recording.wav"  #"/content/Healthy/VA1GGIAORVG47F300320171212.wav"
  st.write("⏳ Processing new patient's embedding vectors...")
  #session_new.new_vecs.append(get_embedding(new_person_file)) #new_vecs
  #session_new.new_labels.append(datetime.now().strftime("%Y-%m-%d\n%H:%M")) #new_labels
