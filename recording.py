# try_recording.py
import streamlit as st
import streamlit.components.v1 as components

def recording():
  st.title("🎙️ Voice Recorder")
  
  recorder_html = """
  <script src="https://cdn.jsdelivr.net/npm/@ffmpeg/ffmpeg@0.12.7/dist/umd/ffmpeg.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@ffmpeg/util@0.12.1/dist/umd/index.min.js"></script>
  
  <div style="padding: 20px; font-family: sans-serif;">
      <button id="startBtn" style="padding: 12px 24px; font-size: 16px; background-color: #e74c3c; color: white; border: none; border-radius: 8px; cursor: pointer;">
          🎙️ Start Recording
      </button>
      <button id="stopBtn" disabled style="padding: 12px 24px; font-size: 16px; background-color: #95a5a6; color: white; border: none; border-radius: 8px; cursor: pointer; margin-left: 10px;">
          ⏹️ Stop
      </button>
      <p id="status" style="margin-top: 15px; font-weight: bold;"></p>
      <audio id="audioPlayer" controls style="display: none; margin-top: 15px; width: 100%;"></audio>
      <a id="downloadLink" style="display: none; margin-top: 10px; padding: 10px 20px; background-color: #27ae60; color: white; text-decoration: none; border-radius: 5px;">
          📥 Download WAV
      </a>
  </div>
  
  <script>
  let mediaRecorder;
  let audioChunks = [];
  
  document.getElementById('startBtn').onclick = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      
      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
      
      mediaRecorder.onstop = async () => {
          document.getElementById('status').innerText = '⏳ Converting to WAV...';
          
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          
          // Decode and convert to WAV using Web Audio API
          const arrayBuffer = await audioBlob.arrayBuffer();
          const audioContext = new AudioContext({ sampleRate: 16000 });
          const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
          
          // Convert to WAV
          const wavBlob = audioBufferToWav(audioBuffer);
          
          // Display and enable download
          const url = URL.createObjectURL(wavBlob);
          document.getElementById('audioPlayer').src = url;
          document.getElementById('audioPlayer').style.display = 'block';
          document.getElementById('downloadLink').href = url;
          document.getElementById('downloadLink').download = 'recording.wav';
          document.getElementById('downloadLink').style.display = 'inline-block';
          document.getElementById('status').innerText = '✅ Done! Click to download.';
      };
      
      mediaRecorder.start();
      document.getElementById('status').innerText = '🔴 Recording...';
      document.getElementById('startBtn').disabled = true;
      document.getElementById('stopBtn').disabled = false;
      document.getElementById('stopBtn').style.backgroundColor = '#e74c3c';
  };
  
  document.getElementById('stopBtn').onclick = () => {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
      document.getElementById('startBtn').disabled = false;
      document.getElementById('stopBtn').disabled = true;
      document.getElementById('stopBtn').style.backgroundColor = '#95a5a6';
  };
  
  // WAV encoder function
  function audioBufferToWav(buffer) {
      const numChannels = 1;
      const sampleRate = buffer.sampleRate;
      const format = 1; // PCM
      const bitDepth = 16;
      
      const data = buffer.getChannelData(0);
      const dataLength = data.length * (bitDepth / 8);
      const headerLength = 44;
      const totalLength = headerLength + dataLength;
      
      const arrayBuffer = new ArrayBuffer(totalLength);
      const view = new DataView(arrayBuffer);
      
      // WAV header
      writeString(view, 0, 'RIFF');
      view.setUint32(4, totalLength - 8, true);
      writeString(view, 8, 'WAVE');
      writeString(view, 12, 'fmt ');
      view.setUint32(16, 16, true);
      view.setUint16(20, format, true);
      view.setUint16(22, numChannels, true);
      view.setUint32(24, sampleRate, true);
      view.setUint32(28, sampleRate * numChannels * (bitDepth / 8), true);
      view.setUint16(32, numChannels * (bitDepth / 8), true);
      view.setUint16(34, bitDepth, true);
      writeString(view, 36, 'data');
      view.setUint32(40, dataLength, true);
      
      // Write audio data
      let offset = 44;
      for (let i = 0; i < data.length; i++) {
          const sample = Math.max(-1, Math.min(1, data[i]));
          view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
          offset += 2;
      }
      
      return new Blob([arrayBuffer], { type: 'audio/wav' });
  }
  
  function writeString(view, offset, string) {
      for (let i = 0; i < string.length; i++) {
          view.setUint8(offset + i, string.charCodeAt(i));
      }
  }
  </script>
  """
  
  components.html(recorder_html, height=250)
  
  st.info("💡 Recording and conversion happens in your browser - no server upload needed!")
