"""
字串 - 進階練習解答
====================
"""

# ============================================================
# 練習 1：字串基本操作（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：字串基本操作】")
print("=" * 40)

text = "Hello, Python World!"

print(f"原始字串：{text}")
print(f"大寫：{text.upper()}")
print(f"小寫：{text.lower()}")
print(f"長度：{len(text)}")
print(f"字母 'o' 出現次數：{text.count('o')}")
print(f"'Python' 的位置：{text.find('Python')}")


# ============================================================
# 練習 2：字串處理（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：字串處理】")
print("=" * 40)

name = input("請輸入姓名：")

# 去除空白
stripped = name.strip()
print(f"去除空白：{stripped}")

# 首字母大寫
titled = stripped.title()
print(f"首字母大寫：{titled}")

# 替換空格
replaced = titled.replace(" ", "!")
print(f"替換空格：{replaced}")

# 反轉字串
reversed_str = titled[::-1]
print(f"反轉字串：{reversed_str}")


# ============================================================
# 練習 3：密碼驗證器（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：密碼驗證器】")
print("=" * 40)

password = input("請輸入密碼：")

# 檢查各項條件
has_length = len(password) >= 8
has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any(c in "!@#$%^&*" for c in password)

# 顯示結果
print(f"{'✓' if has_length else '✗'} 長度足夠")
print(f"{'✓' if has_upper else '✗'} 包含大寫字母")
print(f"{'✓' if has_lower else '✗'} 包含小寫字母")
print(f"{'✓' if has_digit else '✗'} 包含數字")
print(f"{'✓' if has_special else '✗'} 包含特殊字元")

# 計算強度
score = sum([has_length, has_upper, has_lower, has_digit, has_special])
if score == 5:
    strength = "強"
elif score >= 3:
    strength = "中"
else:
    strength = "弱"

print(f"密碼強度：{strength}")


# ============================================================
# 練習 4：文字統計器（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 4：文字統計器】")
print("=" * 40)

text = input("請輸入一段文字：")

# 統計
total_chars = len(text)
no_space_chars = len(text.replace(" ", ""))
words = text.split()
word_count = len(words)

# 統計句子（以 . ! ? 結尾）
sentence_count = text.count('.') + text.count('!') + text.count('?')

# 找最長單字（移除標點）
import string
clean_words = [word.strip(string.punctuation) for word in words]
longest_word = max(clean_words, key=len) if clean_words else ""

print("\n【文字統計】")
print(f"總字元數（含空格）：{total_chars}")
print(f"總字元數（不含空格）：{no_space_chars}")
print(f"單字數量：{word_count}")
print(f"句子數量：{sentence_count}")
print(f"最長的單字：{longest_word}")


# ============================================================
# 練習 5：凱薩密碼（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 5：凱薩密碼】")
print("=" * 40)

def caesar_cipher(text, shift, encrypt=True):
    """凱薩密碼加密/解密"""
    if not encrypt:
        shift = -shift

    result = []
    for char in text:
        if char.isalpha():
            # 判斷大小寫
            base = ord('A') if char.isupper() else ord('a')
            # 計算偏移後的字元
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)

    return ''.join(result)


text = input("請輸入文字：")
shift = int(input("請輸入偏移量："))

encrypted = caesar_cipher(text, shift, encrypt=True)
decrypted = caesar_cipher(encrypted, shift, encrypt=False)

print(f"加密結果：{encrypted}")
print(f"解密結果：{decrypted}")


# ============================================================
# 【字串方法整理】
# ============================================================
"""
【大小寫轉換】
str.upper()      轉大寫
str.lower()      轉小寫
str.title()      每個單字首字母大寫
str.capitalize() 第一個字母大寫
str.swapcase()   大小寫互換

【搜尋】
str.find(sub)    找子字串，返回索引（找不到返回 -1）
str.index(sub)   找子字串，返回索引（找不到拋出異常）
str.count(sub)   計算子字串出現次數
str.startswith() 是否以指定字串開頭
str.endswith()   是否以指定字串結尾

【修改】
str.strip()      去除前後空白
str.replace()    替換字串
str.split()      分割字串成列表
str.join()       用字串連接列表

【檢查】
str.isalpha()    是否全為字母
str.isdigit()    是否全為數字
str.isalnum()    是否全為字母或數字
str.isupper()    是否全為大寫
str.islower()    是否全為小寫
"""
