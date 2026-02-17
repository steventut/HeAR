# Demo 2: I will simulate a new pd patient, talk to cell phone with shaky voice
import streamlit as st
from scipy.spatial.distance import euclidean
from datetime import datetime

session_new = st.session_state  #keep new patients' 6 info
if 'new_vecs' not in session_state_new:
  session_new.new_vecs = []
  session_new.new_labels = []
  session_new.new_distances = []
  session_new.new_jitters = []
  session_new.new_shimmers = []
  session_new.new_updrs_scores = []

def new_patients():
  # --- 4. PROCESS NEW PERSON ---
  st.write (f"--- 🔍 Analyzing New Input: new_person_file ---")
  new_person_file = "recording.wav"  #"/content/Healthy/VA1GGIAORVG47F300320171212.wav"
  st.write("⏳ Processing new patient's embedding vectors...")
  session_new.new_vecs.append(get_embedding(new_person_file)) #new_vecs
  session_new.new_labels.append(datetime.now().strftime("%Y-%m-%d\n%H:%M")) #new_labels
