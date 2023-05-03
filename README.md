# vr_voice_chat
### docker内でのinstallされたモジュール確認方法
```bash
pip freeze | grep <モジュール名>
```
### dockerのコンテナでマウントしたフォルダへのuser権限付与
```bash
sudo chown -R $USER:$USER ./<マウントしたフォルダ名>
```
### gitignoreが反映されない場合
```bash
git rm -r --cached [ファイル名]
```
### WSLを使用しているとpyaudioが使用できない問題
WSL上では録音するためのデバイスを認識できないためエラーが出る
おそらくLinuxで録音するためのデバイスを設定することが必要