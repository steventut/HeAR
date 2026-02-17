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

###### HeAR: new_patients
###### HeAR: new_patients
def new_patients():
  # --- 4. PROCESS NEW PERSON ---
  session_new.demo_stage = "Ahh: Capturing Voice Biomarker" #New patient comeing in for healthy and PD progression check
  Login_huggingface_and_Load_HeAR_model()
  loaded_model = Load_HeAR_model()
  st.write (f"--- 🔍 Analyzing New Input: new_person_file ---")
  new_person_file = "recording.wav"  #"/content/Healthy/VA1GGIAORVG47F300320171212.wav"
  st.write("⏳ Processing new patient's embedding vectors...")
  session_new.new_vecs.append(get_embedding(new_person_file, loaded_model)) #new_vecs
  st.write(session_new.new_vecs)
  session_new.new_labels.append(datetime.now().strftime("%Y-%m-%d\n%H:%M")) #new_labels
