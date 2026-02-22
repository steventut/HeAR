# Demo 2: I will simulate a new pd patient, talk to cell phone with shaky voice
import streamlit as st
import pandas as pd
from scipy.spatial.distance import euclidean
from datetime import datetime
import parselmouth
from parselmouth.praat import call

session_new = st.session_state  #keep new patients' 6 info
if 'new_vecs' not in session_new:
  session_new.demo_stage = "Baseline Model"
  session_new.new_vecs = []
  session_new.new_labels = []
  session_new.new_distances = []
  session_new.new_jitters = []
  session_new.new_shimmers = []
  session_new.new_updrs_scores = []

def Login_huggingface_and_Load_HeAR_model():
  #Cell 2: Login to Huggin Face
  from huggingface_hub.utils import HfFolder
  
  if HfFolder.get_token() is None:
      from huggingface_hub import notebook_login
      notebook_login()
  # Cell 5: Load google/HeAR Model
  ##from huggingface_hub import from_pretrained_keras
  
  # Load the model directly from Hugging Face Hub
  ##loaded_model = from_pretrained_keras("google/hear")
  ##st.write("✅ AI Ready.")
  ##return loaded_model


@st.cache_resource
def Load_HeAR_model():
  import os

  # Force using Keras 2
  os.environ["TF_USE_LEGACY_KERAS"] = "1"
  import tf_keras as keras
  from huggingface_hub import snapshot_download
    
  # Download model files
  model_path = snapshot_download(repo_id="google/hear")
    
  # Load with legacy Keras
  loaded_model = keras.models.load_model(model_path)
  st.write("✅ AI google/HeAR Model Ready!")
  return loaded_model
  
@st.cache_resource
def Load_HeAR_mode_temp2l():
  # Cell 5: Load google/HeAR Model, original codes!!
  from huggingface_hub import from_pretrained_keras

  # Load the model directly from Hugging Face Hub
  loaded_model = from_pretrained_keras("google/hear")
  st.write("✅ AI google/HeAR Model Ready!")
  return loaded_model

@st.cache_resource
def Load_HeAR_model_temp():
  import keras
  from huggingface_hub import snapshot_download
    
  # Download model files (cached automatically)
  model_path = snapshot_download(repo_id="google/hear")
    
  # Load as inference-only layer - minimal memory footprint
  loaded_model = keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')
    
  st.write("✅ AI Ready.")
  return loaded_model

#Cell 3: Sample codes from Huggin Face to use google/HeAR (1)
SAMPLE_RATE = 16000  # Samples per second (Hz)
CLIP_DURATION = 2    # Duration of the audio clip in seconds
##CLIP_DURATION = 3    ## Steve: try 3 seconds: AI distances were changed! BUT did not aligh with motor_UPDRS scores!!!
CLIP_LENGTH = SAMPLE_RATE * CLIP_DURATION  # Total number of samples

#Cell 4: Sample codes from Huggin Face to use google/HeAR (2)
import numpy as np
from scipy.io import wavfile
from scipy import signal
from IPython.display import Audio, display

def resample_audio_and_convert_to_mono(
  audio_array: np.ndarray,
  sampling_rate: float,
  new_sampling_rate: float = SAMPLE_RATE,
  ) -> np.ndarray:
  """
  Resamples an audio array to 16kHz and converts it to mono if it has multiple channels.

  Args:
    audio_array: A numpy array representing the audio data.
    sampling_rate: The original sampling rate of the audio.
    new_sampling_rate: Target sampling rate.

  Returns:
    resampled_audio_mono: A numpy array representing the resampled mono audio at 16kHz.
  """
  # Convert to mono if it's multi-channel
  if audio_array.ndim > 1:
    audio_mono = np.mean(audio_array, axis=1)
  else:
    audio_mono = audio_array

  # Resample
  original_sample_count = audio_mono.shape[0]
  new_sample_count = int(round(original_sample_count * (new_sampling_rate / sampling_rate)))
  resampled_audio_mono = signal.resample(audio_mono, new_sample_count)

  return resampled_audio_mono

# Cell 6: Compute embedding vectors for each voice biomarker
import tensorflow as tf
import matplotlib.pyplot as plt

def get_embedding(path, loaded_model):
  # Load file: normal.wav
  with open(path, 'rb') as f:
    original_sampling_rate, audio_array = wavfile.read(f)
  ##print(f"Sample Rate: {original_sampling_rate} Hz")
  ##print(f"Data Shape: {audio_array.shape}")
  ##print(f"Data Type: {audio_array.dtype}")

  ##Play buttom to hear the sound. => Comment out
  audio_array = resample_audio_and_convert_to_mono(audio_array, original_sampling_rate, SAMPLE_RATE)
  ##display(Audio(audio_array, rate=SAMPLE_RATE))

  # This index corresponds to a cough and was determined by hand. In practice, you
  # would need a detector.
  START = 0

  # Add batch dimension
  input_tensor = np.expand_dims(audio_array[START: START + CLIP_LENGTH], axis=0)

  # Load the model directly from Hugging Face Hub
  #loaded_model = from_pretrained_keras("google/hear")

  # Call inference
  infer = lambda audio_array: loaded_model.signatures["serving_default"](x=audio_array)
  output = infer(tf.constant(input_tensor, dtype=tf.float32))

  # Extract the embedding vector
  embedding_vector = output['output_0'].numpy().flatten()
  ##print("Size of embedding vector:", len(embedding_vector))
  return embedding_vector
  
def get_embedding_temp(path, loaded_model):
  # Load file: normal.wav
  with open(path, 'rb') as f:
    original_sampling_rate, audio_array = wavfile.read(f)
  ##print(f"Sample Rate: {original_sampling_rate} Hz")
  ##print(f"Data Shape: {audio_array.shape}")
  ##print(f"Data Type: {audio_array.dtype}")

  ##Play buttom to hear the sound. => Comment out
  audio_array = resample_audio_and_convert_to_mono(audio_array, original_sampling_rate, SAMPLE_RATE)
  ##display(Audio(audio_array, rate=SAMPLE_RATE))

  # This index corresponds to a cough and was determined by hand. In practice, you
  # would need a detector.
  START = 0

  # Add batch dimension
  ##input_tensor = np.expand_dims(audio_array[START: START + CLIP_LENGTH], axis=0)
  # Prepare input tensor (adjust shape based on model requirements)
  #input_tensor = tf.constant(audio_data[np.newaxis, :], dtype=tf.float32)
  input_tensor = tf.constant(audio_array[np.newaxis, :], dtype=tf.float32)

  # Load the model directly from Hugging Face Hub
  #loaded_model = from_pretrained_keras("google/hear")

  # Call inference
  ##infer = lambda audio_array: loaded_model.signatures["serving_default"](x=audio_array)
  ##output = infer(tf.constant(input_tensor, dtype=tf.float32))
  # Call TFSMLayer directly (not via signatures)
  output = loaded_model(input_tensor)

  # Extract embedding - output is a dict
  if isinstance(output, dict):
    # Get the first output key
    key = list(output.keys())[0]
    embedding_vector = output[key].numpy().flatten()  
  else:
    embedding_vector = output.numpy().flatten()    

  # Extract the embedding vector
  ##embedding_vector = output['output_0'].numpy().flatten()
  #st.write("Size of embedding vector:", len(embedding_vector))

  ## Plot the wave => Comment out
  # Plot the embedding vector
  '''plt.figure(figsize=(12, 4))
  plt.plot(embedding_vector2)
  plt.title('Embedding Vector')
  plt.xlabel('Index')
  plt.ylabel('Value')
  plt.grid(True)
  plt.show()'''
  print("✅ Compute embeddings function defined.")
  return embedding_vector

# Cell 9: THE METADATA REGISTRY: Define patient's age and sex
# ==========================================
#  1. THE METADATA REGISTRY (INPUT DATA HERE)
# ==========================================
# FORMAT: "Unique_FileName_Part": [AGE, SEX]
# Sex: 0 = Male, 1 = Female

metadata_registry = {
    # --- EXAMPLES (Replace with your actual data) ---
    ##"Parkinson-01": [68, 0],   # 68 year old Male
    ##"Parkinson-02": [68, 0],   # Same patient, later time
    ##"VA1ABN":       [72, 1],   # 72 year old Female
    ##"VA1lbuairgo":  [65, 0],
    # ... Add your 17 files here ...
    "Parkinson-01-VA1": [50, 0],
    "Parkinson-02-VA2": [50, 0],
    "Parkinson-11-VA1": [63, 1],
    "Parkinson-12-VA2": [63, 1],
    "VA1lbuairgo52M1606161813": [65, 0],
    "VA1lloeroun56F2605161926": [61, 1],
    "VA1rlouscsi77F2605161825": [40, 1],
    "VA1rriovbie49M2605161845": [68, 0],
    "VA1sncihcio44M1606161720": [73, 1],
    "VA1ssacvhei61M1606161744": [56, 1],
    "VA1ubguot_t40M1606161759": [77, 0],
    "VA2lbuairgo52M1606161814": [65, 0],
    "VA2rlouscsi77F2605161825": [40, 1],
    "VA2rriovbie49M2605161845": [68, 0],
    "VA2sncihcio44M1606161721": [73, 0],
    "VA2ssacvhei61M1606161744": [56, 0],
    "VA2ubguot_t40M1606161759": [77, 0],
    ##
    "VA1BCRAISGS48F210320171005": [63, 1], #BRIGIDA C F 69: Healthy
    "VA1APNITNOT56F230320170850": [61, 1], #ANTONIETTA P F 61: Healthy
    "VA1LFEIOONR57F210320171126": [63, 1], #LEONARDO F 60: Healthy
    "VA2AGNIGNEE54F230320171021": [63, 1], #Angela G F 63: Healthy
    #"VA1AGNIGNEE54F230320171020": [63, 1], #Angela G F 63: Healthy
    "VA2GBIAORVI48M230320171236": [69, 0], #Giovanni B M 69:  Healthy
    "Steve-recording-1":  [67, 0],
    "Steve-Simulate-Parkinson-1": [67, 0],
    # DEFAULT (Fallback if file not found in list)
    # DEFAULT (Fallback if file not found in list)
    "DEFAULT":      [65, 0]  #[65, 0]
}

# Cell 10: Predict motor_UPDRS score
## Move the following codes to cell: predict motor_UPDRS score
## Steve: Start processing 4th plot: motor_UPDRS score
def get_demographics(filename):
  """Finds the Age/Sex for a given file based on the registry."""
  for key, val in metadata_registry.items():
    if key in filename:
      return val[0], val[1] # Return Age, Sex
  return metadata_registry["DEFAULT"] # Fallback

# ==========================================
#  2. ACOUSTIC FEATURE EXTRACTOR
# ==========================================
def get_acoustics_pro(path):
  try:
    sound = parselmouth.Sound(path)
    #sound = parselmouth.Sound("recording.wav")
    ##if sound.get_total_duration() < 0.5: return None
    st.write("after 1 retun none!")

    pitch = sound.to_pitch(time_step=0.01, pitch_floor=75.0, pitch_ceiling=600.0)
    if pitch.count_voiced_frames() == 0: return None
    st.write("after 2 retun none!")
    pp = call(sound, "To PointProcess (periodic, cc)", 75.0, 600.0)

    # 1. Jitter
    jitter_pct = call(pp, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3) * 100
    jitter_abs = call(pp, "Get jitter (local, absolute)", 0.0, 0.0, 0.0001, 0.02, 1.3)

    # 2. Shimmer
    shimmer_pct = call([sound, pp], "Get shimmer (local)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6) * 100
    shimmer_db  = call([sound, pp], "Get shimmer (local_dB)", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)

    # 3. Harmonics
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75.0, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0.0, 0.0)
    if hnr < -200: hnr = -200
    nhr = 10 ** (-hnr / 10)

    return [jitter_pct, jitter_abs, shimmer_pct, shimmer_db, nhr, hnr]
  except:
    return None

def get_new_jitter_shimmer_motor_UPDRS_score(f, gbr_model):
  ## Steve: get jitter, shimmer and motor_UPDRS
  st.write("⏳ Processing new patient's jitter, shimmer & predicted motor_UPDRS score...")
  all_files_to_process = [f]
  for f in all_files_to_process:
    # 1. Get Acoustics
    feats = get_acoustics_pro(f)
    st.write("feats):", feats)
    if feats:
      # 2. Get Demographics automatically
      age, sex = get_demographics(f)
  
      # 3. Create Vector: [Age, Sex, Jitter%, JitterAbs, Shim%, ShimDB, NHR, HNR]
      full_vector = np.array([[age, sex] + feats])
  
      # 4. Predict
      pred = gbr_model.predict(full_vector)[0]
      session_new.new_updrs_scores.append(pred) #new_updrs_scores
  
      # Clean label for graph
      ##label = f.split("/")[-1] # Simple filename
      ##final_labels_updrs.append(label)
  
      # Steve: added for new_jitter, new_shimmer
      session_new.new_jitters.append(feats[0]) #new_jitters
      session_new.new_shimmers.append(feats[2]) #new_shimmers
  
      ## double check prediction: mortal_UPDRS score!!
      #st.write(f"File: {label} | Age: {age} | Sex: {sex} -> Pred: {pred:.2f}")
      st.write(f" Jitter: {feats[0]} | Shimmer: {feats[2]} -> motor_UPDRS Predicted: {pred:.2f}")

@st.cache_resource
def Load_motor_UPDRS_model():
  import joblib
  loaded_model = joblib.load('motor_updrs_model.joblib')
  st.write("✅ Motor_UPRDS Model loaded successfully!")
  return loaded_model
  
###### HeAR: new_patients
###### HeAR: new_patients
new_vecs = []
def new_patients():
  # --- 4. PROCESS NEW PERSON ---
  session_new.demo_stage = "Ahh: Capturing Voice Biomarker" #New patient comeing in for healthy and PD progression check
  Login_huggingface_and_Load_HeAR_model()
  loaded_model = Load_HeAR_model()
  st.write (f"--- 🔍 Analyzing New Input: new_person_file ---")
  new_person_file = "recording.wav"  #"/content/Healthy/VA1GGIAORVG47F300320171212.wav" "VA1AGNIGNEE54F230320171020.wav"
  #new_person_file = "VA1GGIAORVG47F300320171212.wav"  # 
  #new_person_file = "VA1AGNIGNEE54F230320171020.wav"  # Excellent 25 0.39 3.7 11.9
  ##"/content/Healthy/VA1GGIAORVG47F300320171212.wav" "VA1AGNIGNEE54F230320171020.wav"
  st.write("⏳ Processing new patient's embedding vectors...")
  session_new.new_vecs.append(get_embedding(new_person_file, loaded_model)) #new_vecs
  #st.write(session_new.new_vecs)
  session_new.new_labels.append(datetime.now().strftime("%Y-%m-%d\n%H:%M")) #new_labels
  loaded_model_motor_UPDRS = Load_motor_UPDRS_model()
  get_new_jitter_shimmer_motor_UPDRS_score(new_person_file, loaded_model_motor_UPDRS) #new jitter_shimmer_motor_UPDRS_score

def Monitoring_Health_History():
  session_new.demo_stage = "Monitoring Health History" # Monitoring Health History
  session_new.new_vecs = []
  session_new.new_labels = []
  session_new.new_distances = []
  session_new.new_jitters = []
  session_new.new_shimmers = []
  session_new.new_updrs_scores = []
  healthy_vectors_7_back = pd.read_csv("healthy_vectors_7.csv")
  healthy_vectors_7 = healthy_vectors_7_back.values.tolist()  
  #session_new.new_vecs.append(healthy_vectors_7) #new_vecs
  session_new.new_vecs = healthy_vectors_7
