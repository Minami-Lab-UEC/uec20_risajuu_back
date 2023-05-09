import json
import time
import requests
import wave
from eng_to_kana import eng_to_kana
import pprint

class GenerateWav:
    def __init__(self):
        # host = 'localhost'
        host = 'host.docker.internal'
        port = 50021
        self.response_url = f'http://{host}:{port}/'
        self.response_data = None

        # WAVファイルをバイト列に変換する

    def set_response_json(self, response_data):
        self.response_data = response_data
    
    def set_voice_feature(self, speedScale=1.0, pitchScale=1.0, intonationScale=1.0, volumeScale=1.0):
        self.voice_feature = json.loads(self.response_data.text)
        self.voice_feature['accent_phrases'][0]['is_interrogative'] = False
        self.voice_feature['speedScale'] = speedScale
        self.voice_feature['pitchScale'] = pitchScale
        self.voice_feature['volumeScale'] = volumeScale
        self.voice_feature['intonationScale'] = intonationScale
    
    def generate_wav(self, text, emotion = 'Normal', strength = 0.0):
        text = eng_to_kana(text)
        if strength < 0.6:
            speakerId = 59
            speedScale= 0.85
            pitchScale = 0.00
            intonationScale= 1.00
            volumeScale = 1.00
        elif emotion == "Joy":
            speakerId = 58
            speedScale= 0.85
            pitchScale = 0.05
            intonationScale= 1.00
            volumeScale = 1.00
        elif emotion == "Sadness":
            speakerId = 60
            speedScale= 0.85
            pitchScale = -0.05
            intonationScale= 1.00
            volumeScale = 1.00
        elif emotion == "Anticipation":
            speakerId = 58
            speedScale= 0.85
            pitchScale = 0.00
            intonationScale= 1.00
            volumeScale = 1.00
        elif emotion == 'Anger':
            speakerId = 58
            speedScale= 1.00
            pitchScale = -0.10
            intonationScale= 2.00
            volumeScale = 1.50
        elif emotion == 'Fear':
            speakerId = 60
            speedScale= 0.70
            pitchScale = -0.10
            intonationScale= 0.50
            volumeScale = 0.60
        elif emotion == 'Disgust':
            speakerId = 59
            speedScale= 0.70
            pitchScale = -0.10
            intonationScale= 2.00
            volumeScale = 0.80
        elif emotion == 'Trust':
            speakerId = 58
            speedScale= 0.85
            pitchScale = 0.00
            intonationScale= 0.75
            volumeScale = 1.00

        params = (
            ('text', text),
            ('speaker', speakerId),
        )

        self.set_response_json(
            requests.post(
                self.response_url + "audio_query",
                params=params
            )
        )

        self.set_voice_feature(speedScale=speedScale, pitchScale=pitchScale, intonationScale=intonationScale, volumeScale=volumeScale)

        self.set_voice_feature(speedScale=1.25, pitchScale=-0.05)
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            self.response_url + "synthesis",
            headers=headers,
            params=params,
            data=json.dumps(self.voice_feature)
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

        return filepath + filename
    
    def get_speaker(self):
        response = requests.get(
            self.response_url + "speakers",
        )
        pprint.pprint(response.json())
        

def main():
    text1 = "こんにちはぼくはずんだもんなのだ" #16文字
    text2 = "Hello、ぼくはずんだもんなのだ。ずんだあろーのようせいなのだ。ずんだあろうはどんなもちもずんだもちにしてしまうのだ。" # 64文字
    text3 = "ぼくってかわいくない?" # 16文字
    emotion = "happiness"
    strength = 0.5
    generate_wav = GenerateWav()
    start = time.time()
    wav = generate_wav.generate_wav(text1, emotion, strength)

    # wavファイル作成
    generate_wav.convert_bytearray_to_wav('voicevox.wav', wav.content)
    elapsed_time = time.time() - start
    print("voicevox_time:{:.3f}".format(elapsed_time))


def speaker():
    generate_wav = GenerateWav()
    generate_wav.get_speaker()


if __name__ == "__main__":
    main() 