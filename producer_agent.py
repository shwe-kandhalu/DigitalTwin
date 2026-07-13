import glob, time, os
from uagents import Agent, Context, Model

class FeatureRequest(Model):
    wav_path: str

class AnnotationResponse(Model):
    wav_path: str
    diagnosis: str
    confidence: float

producer = Agent(name="producer", port=8001, seed="producer_seed")
ANNOTATOR = None  # set after running annotator

@producer.on_event("startup")
async def send_all(ctx: Context):
    for wav in glob.glob(os.path.expanduser("~/Desktop/recordings/*.wav")):
        await ctx.send(ANNOTATOR, FeatureRequest(wav_path=wav))
        time.sleep(0.1)

@producer.on_message(model=AnnotationResponse)
async def receive(ctx: Context, sender: str, msg: AnnotationResponse):
    print(f"{msg.wav_path}: {msg.diagnosis} ({msg.confidence:.2f})")

if __name__=="__main__":
    print("Paste annotator agent address here, then run")
    producer.run()
