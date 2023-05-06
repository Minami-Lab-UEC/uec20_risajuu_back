import re

dic_file = 'eng.dic'
kana_dict = {}
with open(dic_file, mode='r', encoding='utf-8') as f:
  lines = f.readlines()
  for i, line in enumerate(lines):
    line_list = line.replace('\n', '').split(' ')
    kana_dict[line_list[0]] = line_list[1]

reduction=[["It\'s","イッツ"],["I\'m","アイム"],["You\'re","ユーァ"],["He\'s","ヒーィズ"],["She\'s","シーィズ"],["We\'re","ウィーアー"],["They\'re","ゼァー"],["That\'s","ザッツ"],["Who\'s","フーズ"],["Where\'s","フェアーズ"],["I\'d","アイドゥ"],["You\'d","ユードゥ"],["I\'ve","アイブ"],["I\'ll","アイル"],["You\'ll","ユール"],["He\'ll","ヒール"],["She\'ll","シール"],["We\'ll","ウィール"]]

def eng_to_kana(text):
  # 読みたい記号。他の単語と混ざらないように、前後に半角スペースを挟む
  text = text.replace("+"," プラス ").replace("＋"," プラス ").replace("-"," マイナス ").replace("="," イコール ").replace("＝"," イコール ")

  # No.2、No6みたいに、No.の後に数字が続く場合はノーではなくナンバーと読む
  text = re.sub(r'No\.([0-9])',"ナンバー\\1",text)
  text = re.sub(r'No([0-9])',"ナンバー\\1",text)

  # 短縮形の処理
  for red in reduction: text = text.replace(red[0]," "+red[1]+" ")

  # this is a pen.のように、aの後に半角スペース、続いてアルファベットの場合、エーではなくアッと呼ぶ
  text = re.sub(r'a ([a-zA-Z])',"アッ \\1",text)

  # 文を区切る文字は消してはダメなので、前後に半角スペースを挟む
  text = text.replace("."," . ").replace("。"," 。 ").replace("!"," ! ").replace("！"," ！ ")

  # アルファベットとアルファベット以外が近接している時、その間に半角スペースを挟む（この後、英単語を単語ごとに区切るための前準備）
  text_l=list(text)
  for i in range(len(text))[::-1][:-1]:
    if re.compile("[a-zA-Z]").search(text_l[i]) and re.compile("[^a-zA-Z]").search(text_l[i-1]): text_l.insert(i," ")
    elif re.compile("[^a-zA-Z]").search(text_l[i]) and re.compile("[a-zA-Z]").search(text_l[i+-1]): text_l.insert(i," ")

  text = "".join(text_l)

  # 半角スペースや読まなくて良い文字で区切り、各単語の英語をカタカナに変換
  text_split = re.split('[ \,\*\-\_\=\(\)\[\]\'\"\&\$　]',text)
  for i in range(len(text_split)):
    if str.upper(text_split[i]) in kana_dict:
      text_split[i] = kana_dict[str.upper(text_split[i])]

  return (" ".join(text_split))