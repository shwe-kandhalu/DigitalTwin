from uagents import Bureau
from annotator_agent import agent as annotator
from producer_agent import producer

bureau = Bureau(port=8000)
bureau.add(annotator); bureau.add(producer)

if __name__=="__main__":
    bureau.run()
