import numpy as np
import torchaudio

mel_transform = torchaudio.transforms.MelSpectrogram(
    sample_rate=16000, n_mels=64)

def extract_features(wav_path: str) -> np.ndarray:
    waveform, sr = torchaudio.load(wav_path)
    if sr != 16000:
        waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)
    mel = mel_transform(waveform).log2().clamp(-10, 10)
    return mel.numpy().squeeze(0)
