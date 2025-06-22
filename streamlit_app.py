import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import soundfile as sf
import tempfile

st.set_page_config(page_title="COPD Voice Recorder", layout="centered")
st.title("🎤 COPD Audio Recorder")
st.markdown("This tool records your voice for COPD model analysis. No camera access is required.")

# Define audio-only media constraints (avoid webcam prompt)
media_stream_constraints = {
    "audio": True,
    "video": False
}

# Custom audio processor
class AudioProcessor:
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

# Start webrtc streamer with audio-only
ctx = webrtc_streamer(
    key="audio-only",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints=media_stream_constraints,
    audio_processor_factory=AudioProcessor
)

# After recording stops
if ctx.state.playing is False and ctx.audio_processor and ctx.audio_processor.frames:
    st.success("✅ Recording complete!")

    # Combine and save audio
    audio_data = np.concatenate(ctx.audio_processor.frames, axis=1).flatten()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio_data, 48000)
        st.audio(f.name)
        st.info(f"Saved to: `{f.name}`")

        if st.button("🧠 Run COPD Prediction Model"):
            st.warning("Model integration goes here.")
