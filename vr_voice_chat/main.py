from chat import LangChainChat
from emotionAnalysis import EmotionAnalysis
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Query

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
emotionAnalysis_model = EmotionAnalysis(use_japanese=True, use_gpu=False)

@app.post("/api/v1/chat")
async def create_reply(query: Query):
    reply = chat.conversation(query.text)
    if query.emotionAnalysis:
        emotion = emotionAnalysis_model.analyze_emotion(reply["response"], show_fig=False, ret_prob=True)
    return {"response": reply["response"], "emotion": emotion}

def main():
    while True:
        command = input("You：")
        if command == "exit":
            sys.exit()
        output = chat.conversation(command)
        emotion = emotionAnalysis_model.analyze_emotion(output["response"], show_fig=False, ret_prob=True)
        print("AI：", output["response"], "emotion：", emotion)

if __name__ == "__main__":
    main() 