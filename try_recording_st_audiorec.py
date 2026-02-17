# recording.py
import streamlit as st
from st_audiorec import st_audiorec
import os

def recording():
    st.title("🎙️ Voice Recorder2")
    
    # Initialize session state
    if 'audio_saved' not in st.session_state:
        st.session_state.audio_saved = False
    
    # Record audio
    wav_audio_data = st_audiorec()
    
    if wav_audio_data is not None and len(wav_audio_data) > 0:
        # Save directly to file
        with open("recording.wav", "wb") as f:
            f.write(wav_audio_data)
        st.session_state.audio_saved = True
        st.success("✅ Saved: recording.wav")
        st.write(f"📁 File size: {len(wav_audio_data):,} bytes")

recording()
