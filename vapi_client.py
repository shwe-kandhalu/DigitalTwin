import os
import time
import wave
import threading
import webrtcvad
import sounddevice as sd

# === Configuration ===
RATE = 16000
FRAME_DURATION_MS = 30
NUM_CHANNELS = 1
SILENCE_TIMEOUT = 0.5  # not used for auto-stop, kept for sanity
# Change this to your Desktop path
OUTPUT_DIR = os.path.expanduser("~/Desktop/recordings")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize VAD
vad = webrtcvad.Vad(2)
FRAME_SIZE = int(RATE * FRAME_DURATION_MS / 1000)

# Shared state
buffer = bytearray()
recording = False
stop_requested = False

def recorder_loop():
    global buffer, recording, stop_requested

    with sd.RawInputStream(samplerate=RATE, blocksize=FRAME_SIZE,
                           dtype='int16', channels=NUM_CHANNELS) as stream:
        print("🎤 Listening... speak to begin recording. Press Enter to stop.")
        while not stop_requested:
            frame, _ = stream.read(FRAME_SIZE)
            is_speech = vad.is_speech(frame, RATE)

            if not recording and is_speech:
                recording = True
                buffer = bytearray()
                buffer.extend(frame)
                print("🟢 Recording started.")

            elif recording:
                buffer.extend(frame)

    # When stop is requested
    if recording and buffer:
        save_wav(buffer)

def save_wav(buffer):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.wav"
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(NUM_CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(buffer)
    print(f"💾 Saved to Desktop: {path}")

def wait_for_enter():
    global stop_requested
    input()
    stop_requested = True
    print("🛑 Stop requested")

if __name__ == "__main__":
    t_rec = threading.Thread(target=recorder_loop)
    t_key = threading.Thread(target=wait_for_enter)

    t_rec.start()
    t_key.start()

    t_key.join()
    t_rec.join()
    print("✅ Done")
