from uagents import Agent, Context, Model
import torch, numpy as np
from feature_extractor import extract_features
from model import COPDNet

class FeatureRequest(Model):
    wav_path: str

class AnnotationResponse(Model):
    wav_path: str
    diagnosis: str
    confidence: float

device = torch.device("cpu")
net = COPDNet().to(device)
net.load_state_dict(torch.load("copd_cnn.pth", map_location=device))
net.eval()

agent = Agent(name="annotator", port=8002, seed="annotator_seed")

@agent.on_message(model=FeatureRequest, replies=AnnotationResponse)
async def annotate(ctx: Context, sender: str, msg: FeatureRequest):
    feats = extract_features(msg.wav_path)
    xb = torch.from_numpy(feats).unsqueeze(0).unsqueeze(0).float().to(device)
    with torch.no_grad():
        out = net(xb)
        conf = torch.softmax(out,1)[0]
        pred = int(conf.argmax())
    await ctx.send(sender, AnnotationResponse(
        wav_path=msg.wav_path,
        diagnosis="copd" if pred==1 else "healthy",
        confidence=float(conf[pred])
    ))

if __name__=="__main__":
    agent.run()
