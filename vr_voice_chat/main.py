from chat import LangChainChat
from emotionAnalysis import EmotionAnalysis
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query
import json
import numpy as np


app = FastAPI()

# CORS設定
origins = [
    "*"
]

@app.get("/")
async def root():
  return {"greeting": "Hello World!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = LangChainChat()
# use_gpu = Trueは遅くなるので、False推奨
emotionAnalysis_model = EmotionAnalysis(use_japanese=False, use_gpu=False, use_plot=False)
defalt_emotion = {'Joy': 0.0, 'Sadness': 0.0, 'Anticipation': 0.0, 'Surprise': 0.0, 'Anger': 0.0, 'Fear': 0.0, 'Disgust': 0.0, 'Trust': 0.0}

@app.post("/api/v1/chat")
async def create_reply(query: Query):
    reply = chat.conversation(query.text)
    if query.emotion:
        emotion = emotionAnalysis_model.analyze_emotion(reply["response"], show_fig=False, ret_prob=True)
    else:
        emotion = defalt_emotion
    emotion = {k: np.float64(v) for k, v in emotion.items()}
    return {"response": reply["response"], "emotion": json.dumps(emotion)}

def main():
    while True:
        command = input("You：")
        if command == "exit":
            sys.exit()
        output = chat.conversation(command)
        emotion = emotionAnalysis_model.analyze_emotion(output["response"], show_fig=False, ret_prob=True)
        print(type(emotion))
        print("AI：", output["response"], "emotion：", emotion)

if __name__ == "__main__":
    main() 