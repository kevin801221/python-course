#!/usr/bin/env python3
"""
從 30.正则表达式的应用.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
"""
要求：使用者名稱必須由字母、數字或下劃線構成且長度在6~20個字元之間，QQ號是5~12的數字且首位不能為0
"""
import re

username = input('請輸入使用者名稱: ')
qq = input('請輸入QQ號: ')
# match函式的第一個引數是正規表示式字串或正規表示式物件
# match函式的第二個引數是要跟正規表示式做匹配的字串物件
m1 = re.match(r'^[0-9a-zA-Z_]{6,20}$', username)
if not m1:
    print('請輸入有效的使用者名稱.')
# fullmatch函式要求字串和正規表示式完全匹配
# 所以正規表示式沒有寫起始符和結束符
m2 = re.fullmatch(r'[1-9]\d{4,11}', qq)
if not m2:
    print('請輸入有效的QQ號.')
if m1 and m2:
    print('你輸入的資訊是有效的!')
# === 範例 2 ===
import re

# 建立正規表示式物件，使用了前瞻和回顧來保證手機號前後不應該再出現數字
pattern = re.compile(r'(?<=\D)1[34578]\d{9}(?=\D)')
sentence = '''重要的事情說8130123456789遍，我的手機號是13512346789這個靚號，
不是15600998765，也不是110或119，王大錘的手機號才是15600998765。'''
# 方法一：查詢所有匹配並儲存到一個列表中
tels_list = re.findall(pattern, sentence)
for tel in tels_list:
    print(tel)
print('--------華麗的分隔線--------')

# 方法二：透過迭代器取出匹配物件並獲得匹配的內容
for temp in pattern.finditer(sentence):
    print(temp.group())
print('--------華麗的分隔線--------')

# 方法三：透過search函式指定搜尋位置找出所有匹配
m = pattern.search(sentence)
while m:
    print(m.group())
    m = pattern.search(sentence, m.end())
# === 範例 3 ===
import re

sentence = 'Oh, shit! 你是傻逼嗎? Fuck you.'
purified = re.sub('fuck|shit|[傻煞沙][比筆逼叉缺吊碉雕]',
                  '*', sentence, flags=re.IGNORECASE)
print(purified)  # Oh, *! 你是*嗎? * you.
# === 範例 4 ===
import re

poem = '窗前明月光，疑是地上霜。舉頭望明月，低頭思故鄉。'
sentences_list = re.split(r'[，。]', poem)
sentences_list = [sentence for sentence in sentences_list if sentence]
for sentence in sentences_list:
    print(sentence)
