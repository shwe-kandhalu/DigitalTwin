import torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader, random_split
from dataset import COPDDataset
from model import COPDNet
from sklearn.metrics import classification_report

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ds = COPDDataset("data/")
train_len = int(0.8*len(ds))
train_ds, val_ds = random_split(ds, [train_len, len(ds)-train_len])
train_dl = DataLoader(train_ds,16,shuffle=True)
val_dl = DataLoader(val_ds,16)

model = COPDNet().to(device)
opt, crit = optim.Adam(model.parameters(),1e-3), nn.CrossEntropyLoss()

for epoch in range(20):
    model.train()
    for xb, yb in train_dl:
        xb, yb = xb.to(device), yb.to(device)
        opt.zero_grad()
        loss = crit(model(xb), yb)
        loss.backward(); opt.step()
    print(f"Epoch {epoch+1} done")

model.eval()
preds, trues = [],[]
with torch.no_grad():
    for xb, yb in val_dl:
        xb = xb.to(device)
        out = model(xb)
        preds.extend(out.argmax(1).cpu().numpy())
        trues.extend(yb.numpy())
print(classification_report(trues, preds, target_names=["healthy","copd"]))
torch.save(model.state_dict(), "copd_cnn.pth")
