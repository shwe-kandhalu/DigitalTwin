import os, torch, torchaudio
from torch.utils.data import Dataset

class COPDDataset(Dataset):
    def __init__(self, root_dir):
        self.samples = []
        for label in ["copd", "healthy"]:
            for fname in os.listdir(os.path.join(root_dir, label)):
                if fname.endswith(".wav"):
                    self.samples.append((os.path.join(root_dir, label, fname), 1 if label=="copd" else 0))
        self.mel_transform = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_mels=64)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        waveform, sr = torchaudio.load(path)
        if sr != 16000:
            waveform = torchaudio.transforms.Resample(sr, 16000)(waveform)
        mel = self.mel_transform(waveform).log2().clamp(-10, 10)
        return mel.unsqueeze(0), label
