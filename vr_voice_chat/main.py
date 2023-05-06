from chat import LangChainChat
from emotionAnalysis import EmotionAnalysis
from voicevox import GenerateWav
import sys
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, JSONResponse
from models import Query
import json
import numpy as np
from io import BytesIO
import base64

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
        filepath = wavBinary_encoder.convert_bytearray_to_wav("voicevox.wav", wav_bytes.content)
    else:
        wav_file = None

    # dataを含めたJSONデータを生成する
    data = {
        "text": reply["response"],
        "emotion": emotion,
        "strength": strength,
    }
    with open(filepath, "rb") as wav_file:
          wav_bytes = wav_file.read()
    wav_file = BytesIO(wav_bytes)
    with open(filepath, "rb") as file:
        contents = file.read()
    encoded_wav = base64.b64encode(contents)

    # レスポンスボディにバイナリデータとJSONデータを含める
    content = b"".join(wav_file)
    content_type = "audio/wav"
    headers = {"Content-Disposition": "attachment; filename=audio.wav",}
    response = Response(content, media_type=content_type, headers=headers)
    
    return {"file": encoded_wav, "data": data}

    # json_dict = {"response": reply["response"], "emotion": emotion, "strength": strength}
    # json_str = json.dumps(json_dict)
    # json_bytes = json_str.encode("utf-8")
    # json_file = BytesIO(json_bytes)
        
    # # WAVファイルの読み込み
    # with open(filepath, "rb") as wav_file:
    #     wav_bytes = wav_file.read()
    # wav_file = BytesIO(wav_bytes)

    # json_content = json_file.read()
    # wav_content = wav_file.read()

    # # レスポンスの作成
    # return StreamingResponse(iter([json_content, wav_content]), media_type="multipart/form-data")
    # #return {"response": reply["response"], "emotion": emotion, "strength": strength, "voicevox": wav_file.read()}

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