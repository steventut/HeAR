# recording.py
import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def recording():
    st.title("🎙️ Voice Recorder")
    
    # Fast client-side recorder
    recorder_html = """
    <div style="padding: 10px; font-family: sans-serif;">
        <button id="startBtn" onclick="startRec()" style="padding: 10px 20px; font-size: 14px; background: #e74c3c; color: white; border: none; border-radius: 5px; cursor: pointer;">🎙️ Start</button>
        <button id="stopBtn" onclick="stopRec()" disabled style="padding: 10px 20px; font-size: 14px; background: #95a5a6; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 5px;">⏹️ Stop</button>
        <button id="saveBtn" onclick="saveRec()" disabled style="padding: 10px 20px; font-size: 14px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 5px;">💾 Save</button>
        <p id="status" style="margin-top: 10px; font-weight: bold;"></p>
        <audio id="player" controls style="display:none; margin-top: 10px; width: 100%;"></audio>
    </div>
    <script>
    let mediaRecorder, chunks = [], wavBlob = null;
    
    async function startRec() {
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        mediaRecorder = new MediaRecorder(stream);
        chunks = [];
        mediaRecorder.ondataavailable = e => chunks.push(e.data);
        mediaRecorder.onstop = async () => {
            document.getElementById('status').innerText = '⏳ Converting...';
            const blob = new Blob(chunks, {type: 'audio/webm'});
            const buf = await blob.arrayBuffer();
            const ctx = new AudioContext({sampleRate: 16000});
            const audio = await ctx.decodeAudioData(buf);
            wavBlob = toWav(audio);
            document.getElementById('player').src = URL.createObjectURL(wavBlob);
            document.getElementById('player').style.display = 'block';
            document.getElementById('saveBtn').disabled = false;
            document.getElementById('saveBtn').style.background = '#27ae60';
            document.getElementById('status').innerText = '✅ Ready! Click Save to continue.';
        };
        mediaRecorder.start();
        document.getElementById('status').innerText = '🔴 Recording...';
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('stopBtn').style.background = '#e74c3c';
    }
    
    function stopRec() {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('stopBtn').style.background = '#95a5a6';
    }
    
    function saveRec() {
        if (!wavBlob) return;
        document.getElementById('status').innerText = '⏳ Uploading...';
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64 = reader.result.split(',')[1];
            // Copy to clipboard for manual paste
            navigator.clipboard.writeText(base64).then(() => {
                document.getElementById('status').innerText = '✅ Copied! Paste below and press Enter.';
            });
        };
        reader.readAsDataURL(wavBlob);
    }
    
    function toWav(buffer) {
        const ch = 1, sr = buffer.sampleRate, bps = 16;
        const data = buffer.getChannelData(0);
        const len = data.length * 2 + 44;
        const buf = new ArrayBuffer(len);
        const v = new DataView(buf);
        const s = (o, str) => { for(let i=0; i<str.length; i++) v.setUint8(o+i, str.charCodeAt(i)); };
        s(0,'RIFF'); v.setUint32(4,len-8,true); s(8,'WAVE'); s(12,'fmt ');
        v.setUint32(16,16,true); v.setUint16(20,1,true); v.setUint16(22,ch,true);
        v.setUint32(24,sr,true); v.setUint32(28,sr*ch*bps/8,true);
        v.setUint16(32,ch*bps/8,true); v.setUint16(34,bps,true);
        s(36,'data'); v.setUint32(40,data.length*2,true);
        for(let i=0,o=44; i<data.length; i++,o+=2) {
            const sample = Math.max(-1, Math.min(1, data[i]));
            v.setInt16(o, sample<0 ? sample*0x8000 : sample*0x7FFF, true);
        }
        return new Blob([buf], {type:'audio/wav'});
    }
    </script>
    """
    
    # Component without key parameter
    components.html(recorder_html, height=180)
    
    # Text input to receive pasted base64 data
    audio_input = st.text_input("Paste audio data here:", key="audio_data")
    
    if audio_input and len(audio_input) > 100:
        try:
            audio_bytes = base64.b64decode(audio_input)
            with open("recording.wav", "wb") as f:
                f.write(audio_bytes)
            st.success(f"✅ Saved: recording.wav ({len(audio_bytes):,} bytes)")
            st.audio(audio_bytes, format='audio/wav')
        except Exception as e:
            st.error(f"Error: {e}")

# Run
if __name__ == "__main__":
    recording()
