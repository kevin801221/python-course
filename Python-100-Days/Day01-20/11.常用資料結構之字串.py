#!/usr/bin/env python3
"""
從 11.常用数据结构之字符串.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
s1 = 'hello, world!'
s2 = "你好，世界！❤️"
s3 = '''hello,
wonderful
world!'''
print(s1)
print(s2)
print(s3)
# === 範例 2 ===
s1 = '\'hello, world!\''
s2 = '\\hello, world!\\'
print(s1)
print(s2)
# === 範例 3 ===
s1 = '\it \is \time \to \read \now'
s2 = r'\it \is \time \to \read \now'
print(s1)
print(s2)
# === 範例 4 ===
s1 = '\141\142\143\x61\x62\x63'
s2 = '\u9a86\u660a'
print(s1)
print(s2)
# === 範例 5 ===
s1 = 'hello' + ', ' + 'world'
print(s1)    # hello, world
s2 = '!' * 3
print(s2)    # !!!
s1 += s2
print(s1)    # hello, world!!!
s1 *= 2
print(s1)    # hello, world!!!hello, world!!!
# === 範例 6 ===
s1 = 'a whole new world'
s2 = 'hello world'
print(s1 == s2)             # False
print(s1 < s2)              # True
print(s1 == 'hello world')  # False
print(s2 == 'hello world')  # True
print(s2 != 'Hello world')  # True
s3 = 'Kevin'
print(ord('駱'))            # 39558
print(ord('昊'))            # 26122
s4 = '王大錘'
print(ord('王'))            # 29579
print(ord('大'))            # 22823
print(ord('錘'))            # 38180
print(s3 >= s4)             # True
print(s3 != s4)             # True
# === 範例 7 ===
s1 = 'hello, world'
s2 = 'goodbye, world'
print('wo' in s1)      # True
print('wo' not in s2)  # False
print(s2 in s1)        # False
# === 範例 8 ===
s = 'hello, world'
print(len(s))                 # 12
print(len('goodbye, world'))  # 14
# === 範例 9 ===
s = 'abc123456'
n = len(s)
print(s[0], s[-n])    # a a
print(s[n-1], s[-1])  # 6 6
print(s[2], s[-7])    # c c
print(s[5], s[-4])    # 3 3
print(s[2:5])         # c12
print(s[-7:-4])       # c12
print(s[2:])          # c123456
print(s[:2])          # ab
print(s[::2])         # ac246
print(s[::-1])        # 654321cba
# === 範例 10 ===
s = 'hello'
for i in range(len(s)):
    print(s[i])
# === 範例 11 ===
s = 'hello'
for elem in s:
    print(elem)
# === 範例 12 ===
s1 = 'hello, world!'
# 字串首字母大寫
print(s1.capitalize())  # Hello, world!
# 字串每個單詞首字母大寫
print(s1.title())       # Hello, World!
# 字串變大寫
print(s1.upper())       # HELLO, WORLD!
s2 = 'GOODBYE'
# 字串變小寫
print(s2.lower())       # goodbye
# 檢查s1和s2的值
print(s1)               # hello, world
print(s2)               # GOODBYE
# === 範例 13 ===
s = 'hello, world!'
print(s.find('or'))      # 8
print(s.find('or', 9))   # -1
print(s.find('of'))      # -1
print(s.index('or'))     # 8
print(s.index('or', 9))  # ValueError: substring not found
# === 範例 14 ===
s = 'hello world!'
print(s.find('o'))       # 4
print(s.rfind('o'))      # 7
print(s.rindex('o'))     # 7
# print(s.rindex('o', 8))  # ValueError: substring not found
# === 範例 15 ===
s1 = 'hello, world!'
print(s1.startswith('He'))   # False
print(s1.startswith('hel'))  # True
print(s1.endswith('!'))      # True
s2 = 'abc123456'
print(s2.isdigit())  # False
print(s2.isalpha())  # False
print(s2.isalnum())  # True
# === 範例 16 ===
s = 'hello, world'
print(s.center(20, '*'))  # ****hello, world****
print(s.rjust(20))        #         hello, world
print(s.ljust(20, '~'))   # hello, world~~~~~~~~
print('33'.zfill(5))      # 00033
print('-33'.zfill(5))     # -0033
# === 範例 17 ===
a = 321
b = 123
print('%d * %d = %d' % (a, b, a * b))
# === 範例 18 ===
a = 321
b = 123
print('{0} * {1} = {2}'.format(a, b, a * b))
# === 範例 19 ===
a = 321
b = 123
print(f'{a} * {b} = {a * b}')
# === 範例 20 ===
s1 = '   jackfrued@126.com  '
print(s1.strip())      # jackfrued@126.com
s2 = '~你好，世界~'
print(s2.lstrip('~'))  # 你好，世界~
print(s2.rstrip('~'))  # ~你好，世界
# === 範例 21 ===
s = 'hello, good world'
print(s.replace('o', '@'))     # hell@, g@@d w@rld
print(s.replace('o', '@', 1))  # hell@, good world
# === 範例 22 ===
s = 'I love you'
words = s.split()
print(words)            # ['I', 'love', 'you']
print('~'.join(words))  # I~love~you
# === 範例 23 ===
s = 'I#love#you#so#much'
words = s.split('#')
print(words)  # ['I', 'love', 'you', 'so', 'much']
words = s.split('#', 2)
print(words)  # ['I', 'love', 'you#so#much']
# === 範例 24 ===
a = 'Kevin'
b = a.encode('utf-8')
c = a.encode('gbk')
print(b)                  # b'\xe9\xaa\x86\xe6\x98\x8a'
print(c)                  # b'\xc2\xe6\xea\xbb'
print(b.decode('utf-8'))  # Kevin
print(c.decode('gbk'))    # Kevin
