# uec20_risaju_backwend
## 自分用コマンドまとめ
- docker内でのinstallされたモジュール確認方法
```bash
pip freeze | grep <モジュール名>
```
- dockerのコンテナでマウントしたフォルダへのuser権限付与
```bash
sudo chown -R $USER:$USER ./<マウントしたフォルダ名>
```
- gitignoreが反映されない場合
```bash
git rm -r --cached [ファイル名]
```
## Issue
- WSLを使用しているとpyaudioが使用できない問題\
WSL上では録音するためのデバイスを認識できないためエラーが出る
おそらくLinuxで録音するためのデバイスを設定することが必要

## backendServerの起動方法
- dockerの起動
```bash
docker-compose up -d
```
- dockerコンテナに入る
```bash
docker-compose exec app bash
```
- fastAPIサーバーの起動
    - vr_voice_chatフォルダ内に.envファイルを作成
    - .envファイルに以下を記述
        ```bash
        OPENAI_API_KEY=<openaiのAPIキー>
        ```
    - dockerコンテナ内で
        ```bash
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ```
    - 以下にアクセスしてHello Worldが表示されれば成功
        http://localhost:8080/
- APIの確認
    - 以下にアクセスしてAPIの仕様が表示されれば成功
http://localhost:8080/docs
## 感情分析APIの使用方法
- emotion-analysis-modelをダウンロード
- vr_voice_chatフォルダ内にemotion-analysis-modelフォルダを配置
- パラメータの意味
    - APIパラメータ
        - query.text (str): userの発言
        - emotionAnalysis (bool) : 感情分析を行うかどうか
    - EmotionAnalysisクラスのパラメータ
        - use_japanese (bool): 感情のラベル日本語かするかどうか
        - use_gpu (bool) : GPUを使用するかどうか