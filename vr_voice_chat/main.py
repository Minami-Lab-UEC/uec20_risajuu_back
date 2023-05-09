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
import time
import wave

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

class BaseClass:
    def __init__(self, use_gpu=False, use_japanese=False, use_plot=False):
        self.chat = LangChainChat()
        self.emotionAnalysis_model = EmotionAnalysis(use_japanese=False, use_gpu=False, use_plot=False)
        self.wavBinary_encoder = GenerateWav()
        self.filepath = None
    
    def set_filepath(self, filepath):
        self.filepath = filepath
    
    def get_filepath(self):
        return self.filepath

base = BaseClass()

@app.post("/api/v1/chat")
async def create_reply(query: Query):
    reply = base.chat.conversation(query.text)
    if query.emotion:
        emotion, strength = base.emotionAnalysis_model.analyze_emotion(reply["response"], show_fig=False, ret_prob=True)
    else:
        emotion, strength = None, None
    
    if query.voicevox:
        # TODO wavファイルをバイト列に変換する
        wav_bytes = (base.wavBinary_encoder.generate_wav(reply["response"], emotion, strength))
        base.set_filepath(base.wavBinary_encoder.convert_bytearray_to_wav("voicevox.wav", wav_bytes.content))
    
    # dataを含めたJSONデータを生成する
    dict = {
        "text": reply["response"],
        "emotion": emotion,
        "strength": strength,
    }

    json_dict = json.dumps(dict)
    json_data = json_dict.encode("utf-8")
    if query.return_wav:
        with open(base.get_filepath(), "rb") as file:
            contents = file.read()
        encoded_wav = base64.b64encode(contents)
        return {"file": encoded_wav, "data": json_data}
    
    else:
        return json_data

    # with open(filepath, "rb") as wav_file:
    #       wav_bytes = wav_file.read()
    # wav_file = BytesIO(wav_bytes)

    # レスポンスボディにバイナリデータとJSONデータを含める
    # content = b"".join(wav_file)
    # content_type = "audio/wav"
    # headers = {"Content-Disposition": "attachment; filename=audio.wav",}
    # response = Response(content, media_type=content_type, headers=headers)

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

@app.post("/api/v1/wav")
async def send_wav():
    base.set_filepath("./audio_data/voicevox.wav")
    print(base.get_filepath())
    with open(base.get_filepath(), "rb") as wav_file:
           wav_bytes = wav_file.read()
    wav_file = BytesIO(wav_bytes)

    # レスポンスボディにバイナリデータとJSONデータを含める
    content = wav_file.read()
    content_type = "audio/wav"
    headers = {"Content-Disposition": "attachment; filename=audio.wav",}
    response = Response(content, media_type=content_type, headers=headers)
    return response


def main():
    while True:
        command = input("You：")
        if command == "exit":
            sys.exit()
        
        start = time.time()
        output = base.chat.conversation(command)
        elapsed_time = time.time() - start
        print("chat_time:{:.3f}".format(elapsed_time))

        start = time.time()
        emotion, strength = base.emotionAnalysis_model.analyze_emotion(output["response"], show_fig=False, ret_prob=True)
        elapsed_time = time.time() - start
        print("emotion_analysis_time:{:.3f}".format(elapsed_time))

        start = time.time()
        wav_bytes = base.wavBinary_encoder.generate_wav(output["response"], emotion, strength)
        filepath = base.wavBinary_encoder.convert_bytearray_to_wav("voicevox.wav", wav_bytes.content)
        elapsed_time = time.time() - start
        print("voicevox_time:{:.3f}".format(elapsed_time))

        start = time.time()
        with open(filepath, "rb") as file:
            contents = file.read()
        encoded_wav = base64.b64encode(contents)
        elapsed_time = time.time() - start
        print("wav_encorded_time:{:.3f}".format(elapsed_time))

        print("AI：", output["response"], "emotion：", emotion, "strength：", strength)

if __name__ == "__main__":
    main() 