from chat import LangChainChat
from emotionAnalysis import EmotionAnalysis
from voicevox import GenerateWav
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
wavBinary_encoder = GenerateWav()

@app.post("/api/v1/chat")
async def create_reply(query: Query):
    reply = chat.conversation(query.text)
    if query.emotion:
        emotion, strength = emotionAnalysis_model.analyze_emotion(reply["response"], show_fig=False, ret_prob=True)
    else:
        emotion, strength = None, None
    
    if query.voicevox:
        # TODO wavファイルをバイト列に変換する
        wav_bytes = wavBinary_encoder.generate_wav(reply["response"], emotion, strength)
    else:
        wav_bytes = None

    return {"response": reply["response"], "emotion": emotion, "strength": strength, "voicevox": wav_bytes.content}

import wave

def main():
    while True:
        command = input("You：")
        if command == "exit":
            sys.exit()
        output = chat.conversation(command)
        emotion, strength = emotionAnalysis_model.analyze_emotion(output["response"], show_fig=False, ret_prob=True)
        wav_bytes = wavBinary_encoder.generate_wav(output["response"], emotion, strength)
        wavBinary_encoder.convert_bytearray_to_wav("voicevox.wav", wav_bytes.content)
        print("AI：", output["response"], "emotion：", emotion, "strength：", strength)

if __name__ == "__main__":
    main() 