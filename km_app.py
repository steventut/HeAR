### Revision history
## version 1.0 Initial development for google/HeAR app for PD progression Monitoring

import streamlit as st
import recording #2/17/2026
import new_patients #2/17/2026
import time
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean
from datetime import datetime
import matplotlib.pyplot as plt

session_new = st.session_state  #keep new patients' 6 info
if 'new_vecs' not in session_new:
  session_new.demo_stage = "Baseline Model"
  session_new.new_vecs = []
  session_new.new_labels = []
  session_new.new_distances = []
  session_new.new_jitters = []
  session_new.new_shimmers = []
  session_new.new_updrs_scores = []

with st.sidebar:
    #st.title('Parkinson Disease Progression Monitoring using Voice Biomarker')
    st.title('Vocalis-PD: A Multimodal Digital Biomarker Companion for Parkinson’s Therapies')
    st.write('v1.0')

##### HeAR added!
st.set_page_config(
    page_title="Parkinson Disease Progression Monitoring System",
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

    if session_new.demo_stage == "Ahh: Capturing Voice Biomarker": # Demo 2
        session_new.new_distances = []
        for vecs in session_new.new_vecs:
            session_new.new_distances.append(euclidean(vecs, golden_vector)) #new_distances	
        if len(session_new.new_distances) == 1:
            st.write("New patient's AI distance: ", round(session_new.new_distances[0]))
        else:
            st.write("New patient's AI distance: ", round(session_new.new_distances[1]))
        st.title("Dashboard: Monitoring Health Progression")

    # Demo 1: show baseline model (no new patient)
    # --- 5. GENERATE PLOT 1: UPDATED PCA MAP ---
    if session_new.demo_stage == "Baseline Model": # Demo 1
        all_vectors = [golden_vector] + healthy_vectors	 + pd_vectors
    elif session_new.demo_stage == "Ahh: Capturing Voice Biomarker": # Demo 2
        all_vectors = [golden_vector] + healthy_vectors + pd_vectors + session_new.new_vecs
    elif session_new.demo_stage == "Monitoring Health History": # Demo 3
        all_vectors = [golden_vector] + healthy_vectors + pd_vectors + session_new.new_vecs		
	
    pca = PCA(n_components=2)
    all_2d = pca.fit_transform(np.array(all_vectors))

    gold_2d = all_2d[0]
    healthy_2d = all_2d[1:len(healthy_vectors)+1]
    #pd_2d = all_2d[len(healthy_vectors)+1:-1]
    pd_2d = all_2d[1+len(healthy_vectors)+1:1+len(healthy_vectors)+1+len(pd_vectors)]
    
    if session_new.demo_stage == "Ahh: Capturing Voice Biomarker" or \
	    session_new.demo_stage == "Monitoring Health History": # Demo 2, Demo 3
        #new_2d = []
        new_2d = all_2d[-len(session_new.new_vecs):]

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

    # 5. The New Person (Blue Dot) => lebelling
    #if len(new_2d) != 0:
    if session_new.demo_stage == "Ahh: Capturing Voice Biomarker" or \
	    session_new.demo_stage == "Monitoring Health History": # Demo 2, Demo 3
        plt.scatter(new_2d[:,0], new_2d[:,1], c='blue', s=400, edgecolors='white', linewidth=3, zorder=20, label='New Input')
        for i, txt in enumerate(session_new.new_labels):
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

    # Load the data back from the CSV file into a new variable
    df_sorted = pd.read_csv("data_for_4_plots.csv")
    ##print("Successfully loaded 'data_for_4_plots.csv' into df_sorted_back:")
    ## Display the first few rows to verify it loaded correctly
    ##display(df_sorted)

    if session_new.demo_stage == "Ahh: Capturing Voice Biomarker": # Demo 2
        # 1. Combine all variables into a single dictionary, then create a DataFrame
        data = {
          'Label': session_new.new_labels,
          'Distance from Golden Vector': session_new.new_distances,
          'Jitter': session_new.new_jitters,
          'Shimmer': session_new.new_shimmers,
          'Predicted motor_UPDRS': session_new.new_updrs_scores
        }
        #st.write(data)
        df_new = pd.DataFrame(data)
        df_sorted = pd.concat([df_sorted, df_new], ignore_index=True)
        #st.write(df_sorted)

    if session_new.demo_stage == "Monitoring Health History": # Demo 3
        # Load the data back from the CSV file into a new variable
        df_data_for_7_healthy = pd.read_csv("data_for_7_healthy.csv")        
        #st.write(df_data_for_7_healthy)
        df_sorted = pd.concat([df_sorted, df_data_for_7_healthy], ignore_index=True)
        #st.write(df_sorted)	
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

menu_functions = ["Product Description", "Baseline Model","Ahh: Capturing Voice Biomarker", "Monitoring Health History"]
choice_menu = st.sidebar.radio("Menu", menu_functions)
if choice_menu == "Product Description":
    #st.title("Prodcut Description")
    #st.markdown("## Vocalis-PD: A Multimodal Digital Biomarker Companion for Parkinson’s Therapies")
    st.markdown("### Vocalis-PD is a Parkinson Disease Progression Monitoring System using Voice Biomarker generated from google/HeAR model.")
    st.markdown("#### In-person visits to clinics are too slow to check their progression of Parkinson’s Therapies. We developed “A Multimodal Digital Biomarker Companion for Parkinson’s Therapies”, an application to track and monitor the progression of Parkinson’s Therapies. The patients need only speak “Ahh” to a mobile phone, and our Companion App will immediately tell the patients' progression of the Therapies: Whether patients are in the recovering stage or moving away from healthy people. The real time and online progression monitering of the Therapies allows clinicians to adjust treatments dynamically and democratizes access to neurological tracking in under-resourced or rural areas where specialized clinics do not exist.")
elif choice_menu == "Baseline Model": #Demo 1
    session_new.demo_stage = "Baseline Model"
    st.title("Baseline Model")
    st.markdown("### Clustering Voice Biomarker for both Healthy People and Parkinson Patients")
    load_data()
elif choice_menu == "Ahh: Capturing Voice Biomarker": #Demo 2
    recording.recording()
    if st.button("I am ready, continue!"):
        st.write("Processing started...")
        new_patients.new_patients()
        load_data()
elif choice_menu == "Monitoring Health History": #Demo 3
    st.title("Dashboard: Monitoring Health Progression")
    new_patients.Monitoring_Health_History()
    load_data()
    session_new.new_vecs = []
    session_new.new_labels = []
    session_new.new_distances = []
    session_new.new_jitters = []
    session_new.new_shimmers = []
    session_new.new_updrs_scores = []
