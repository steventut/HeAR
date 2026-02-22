# recording.py
import streamlit as st
from streamlit_mic_recorder import mic_recorder
import subprocess
import os

### Ahh: Capturing Voice Biomarker
def recording():
    st.title("🎙️ Voice Recorder")
    st.markdown("### Speak Ahh: Capturing Voice Biomarker")
    
    # Callback to save file immediately when recording stops
    def save_audio():
        if st.session_state.my_recorder_output:
            audio_bytes = st.session_state.my_recorder_output['bytes']
            
            # Save webm first (fast - no conversion)
            with open("recording.webm", "wb") as f:
                f.write(audio_bytes)
            
            # Convert to WAV in background (if needed for your model)
            subprocess.run([
                'ffmpeg', '-y', '-i', 'recording.webm',
                '-ar', '16000', '-ac', '1',
                'recording.wav'
            ], capture_output=True)
            
            st.session_state.audio_saved = True
    
    # Record with webm format (faster than wav)
    audio = mic_recorder(
        start_prompt="🎙️ Start",
        stop_prompt="⏹️ Stop", 
        format="webm",  # Much faster than wav!
        callback=save_audio,
        key="my_recorder"
    )
    
    # Show status
    if st.session_state.get('audio_saved'):
        st.success("✅ Voice File Saved: recording.wav")
        if os.path.exists("recording.wav"):
            st.audio("recording.wav")
            st.write(f"📁 Size: {os.path.getsize('recording.wav'):,} bytes")
