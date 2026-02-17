# recording.py
import streamlit as st
from st_audiorec import st_audiorec

def recording():
    st.title("🎙️ Voice Recorder")
    
    # Record audio
    wav_audio_data = st_audiorec()
    
    if wav_audio_data is not None:
        # Save directly to file
        with open("recording.wav", "wb") as f:
            f.write(wav_audio_data)
        
        st.success("✅ Saved: recording.wav")
        st.audio(wav_audio_data, format='audio/wav')
        
recording()
