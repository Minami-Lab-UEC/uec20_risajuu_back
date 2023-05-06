import json
import requests
import wave
from eng_to_kana import eng_to_kana

class GenerateWav:
    def __init__(self):
        # host = 'localhost'
        host = 'host.docker.internal'
        port = 50021
        self.response_url = f'http://{host}:{port}/'

        # WAVファイルをバイト列に変換する

    def generate_wav(self, text, emotion = 'Normal', strength = 0.0):
        text = eng_to_kana(text)
        params = (
            ('text', text),
            # ToDo emotionによってspeakerを変更
            ('speaker', 1) #ずんだもん あまあま 1
        )

        query = requests.post(
            self.response_url + "audio_query",
            params=params
        )
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            self.response_url + "synthesis",
            headers=headers,
            params=params,
            data=json.dumps(query.json())
        )

        return response


    def convert_wav_to_bytearray(self, filename):
        with wave.open(filename, 'rb') as f:
            # チャンネル数、サンプルサイズ（バイト）、サンプリング周波数、サンプル数、圧縮形式、圧縮形式名を取得する
            channels, sampwidth, framerate, nframes, _, _ = f.getparams()
            # バイト列を読み込む
            frames = f.readframes(nframes)
        # バイト列を返す
        return frames

    def convert_bytearray_to_wav(self, filename, binary):
        filepath = './audio_data/'
        wf = wave.open(filepath + filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(binary)
        wf.close()

def main():
    text = "hello"
    emotion = "happiness"
    strength = 0.5
    generate_wav = Generate_Wav()
    wav = generate_wav.generate_wav(text, emotion, strength)

    # wavファイル作成
    generate_wav.convert_bytearray_to_wav('voicevox.wav', wav.content)

if __name__ == "__main__":
    main() 