# try_recording.py
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import subprocess
import os

st.title("🎙️ Voice Recorder")

# Record audio (returns bytes)
audio_bytes = audio_recorder(
    text="Click to record",
    recording_color="#e74c3c",
    neutral_color="#6c757d",
    icon_size="2x"
)

if audio_bytes:
    # Save as temp webm
    with open("temp.webm", "wb") as f:
        f.write(audio_bytes)
    
    # Convert to WAV using ffmpeg
    subprocess.run([
        'ffmpeg', '-y', '-i', 'temp.webm',
        '-ar', '16000', '-ac', '1',
        'recording.wav'
    ], capture_output=True)
    
    if os.path.exists("temp.webm"):
        os.remove("temp.webm")
    
    st.success("✅ Saved: recording.wav")
    st.audio("recording.wav")
    
    # Download button
    with open("recording.wav", "rb") as f:
        st.download_button(
            label="📥 Download WAV",
            data=f,
            file_name="recording.wav",
            mime="audio/wav"
        )
