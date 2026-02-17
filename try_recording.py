# simple_recorder.py
import streamlit as st
import subprocess
import os
from audiorecorder import audiorecorder

st.title("🎙️ Voice Recorder")

audio = audiorecorder("🎙️ Record", "🔴 Stop")

if len(audio) > 0:
    # Save as temp webm
    audio.export("temp.webm", format="webm")
    
    # Convert to WAV
    subprocess.run([
        'ffmpeg', '-y', '-i', 'temp.webm',
        '-ar', '16000', '-ac', '1',
        'recording.wav'
    ], capture_output=True)
    
    os.remove("temp.webm")
    
    st.success("✅ Saved: recording.wav")
    st.audio("recording.wav")
