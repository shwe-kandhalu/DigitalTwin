import torch.nn as nn

class ECABlock(nn.Module):
    def __init__(self, channel, k_size=3):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.conv = nn.Conv1d(1, 1, k_size, padding=(k_size-1)//2, bias=False)
        self.sig = nn.Sigmoid()

    def forward(self, x):
        y = self.avg_pool(x).squeeze(-1).permute(0,2,1)
        y = self.sig(self.conv(y)).permute(0,2,1).unsqueeze(-1)
        return x * y

class COPDNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,32,3,1,1); self.eca1 = ECABlock(32)
        self.conv2 = nn.Conv2d(32,64,3,1,1); self.eca2 = ECABlock(64)
        self.conv3 = nn.Conv2d(64,128,3,1,1); self.eca3 = ECABlock(128)
        self.pool = nn.MaxPool2d(2,2)
        self.fc = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(128,2))

    def forward(self, x):
        x = self.pool(self.eca1(self.conv1(x)))
        x = self.pool(self.eca2(self.conv2(x)))
        x = self.pool(self.eca3(self.conv3(x)))
        return self.fc(x)
