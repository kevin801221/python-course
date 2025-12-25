#!/usr/bin/env python3
"""
從 13.常用数据结构之字典.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
person1 = ['王大錘', 55, 168, 60, '成都市武侯區科華北路62號1棟101', '13122334455', '13800998877']
person2 = ('王大錘', 55, 168, 60, '成都市武侯區科華北路62號1棟101', '13122334455', '13800998877')
person3 = {'王大錘', 55, 168, 60, '成都市武侯區科華北路62號1棟101', '13122334455', '13800998877'}
# === 範例 2 ===
xinhua = {
    '麓': '山腳下',
    '路': '道，往來通行的地方；方面，地區：南～貨，外～貨；種類：他倆是一～人',
    '蕗': '甘草的別名',
    '潞': '潞水，水名，即今山西省的濁漳河；潞江，水名，即雲南省的怒江'
}
print(xinhua)
person = {
    'name': '王大錘',
    'age': 55,
    'height': 168,
    'weight': 60,
    'addr': '成都市武侯區科華北路62號1棟101', 
    'tel': '13122334455',
    'emergence contact': '13800998877'
}
print(person)
# === 範例 3 ===
# dict函式(構造器)中的每一組引數就是字典中的一組鍵值對
person = dict(name='王大錘', age=55, height=168, weight=60, addr='成都市武侯區科華北路62號1棟101')
print(person)  # {'name': '王大錘', 'age': 55, 'height': 168, 'weight': 60, 'addr': '成都市武侯區科華北路62號1棟101'}

# 可以透過Python內建函式zip壓縮兩個序列並建立字典
items1 = dict(zip('ABCDE', '12345'))
print(items1)  # {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5'}
items2 = dict(zip('ABCDE', range(1, 10)))
print(items2)  # {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}

# 用字典生成式語法建立字典
items3 = {x: x ** 3 for x in range(1, 6)}
print(items3)  # {1: 1, 2: 8, 3: 27, 4: 64, 5: 125}
# === 範例 4 ===
person = {
    'name': '王大錘',
    'age': 55,
    'height': 168,
    'weight': 60,
    'addr': '成都市武侯區科華北路62號1棟101'
}
print(len(person))  # 5
for key in person:
    print(key)
# === 範例 5 ===
person = {
    'name': '王大錘',
    'age': 55,
    'height': 168,
    'weight': 60,
    'addr': ['成都市武侯區科華北路62號1棟101', '北京市西城區百萬莊大街1號'],
    'car': {
        'brand': 'BMW X7',
        'maxSpeed': '250',
        'length': 5170,
        'width': 2000,
        'height': 1835,
        'displacement': 3.0
    }
}
print(person)
# === 範例 6 ===
person = {'name': '王大錘', 'age': 55, 'height': 168, 'weight': 60, 'addr': '成都市武侯區科華北路62號1棟101'}

# 成員運算
print('name' in person)  # True
print('tel' in person)   # False

# 索引運算
print(person['name'])
print(person['addr'])
person['age'] = 25
person['height'] = 178
person['tel'] = '13122334455'
person['signature'] = '你的男朋友是一個蓋世垃圾，他會踏著五彩祥雲去迎娶你的閨蜜'
print(person)

# 迴圈遍歷
for key in person:
    print(f'{key}:\t{person[key]}')
# === 範例 7 ===
person = {'name': '王大錘', 'age': 25, 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
print(person.get('name'))       # 王大錘
print(person.get('sex'))        # None
print(person.get('sex', True))  # True
# === 範例 8 ===
person = {'name': '王大錘', 'age': 25, 'height': 178}
print(person.keys())    # dict_keys(['name', 'age', 'height'])
print(person.values())  # dict_values(['王大錘', 25, 178])
print(person.items())   # dict_items([('name', '王大錘'), ('age', 25), ('height', 178)])
for key, value in person.items():
    print(f'{key}:\t{value}')
# === 範例 9 ===
person1 = {'name': '王大錘', 'age': 55, 'height': 178}
person2 = {'age': 25, 'addr': '成都市武侯區科華北路62號1棟101'}
person1.update(person2)
print(person1)  # {'name': '王大錘', 'age': 25, 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
# === 範例 10 ===
person1 = {'name': '王大錘', 'age': 55, 'height': 178}
person2 = {'age': 25, 'addr': '成都市武侯區科華北路62號1棟101'}
person1 |= person2
print(person1)  # {'name': '王大錘', 'age': 25, 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
# === 範例 11 ===
person = {'name': '王大錘', 'age': 25, 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
print(person.pop('age'))  # 25
print(person)             # {'name': '王大錘', 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
print(person.popitem())   # ('addr', '成都市武侯區科華北路62號1棟101')
print(person)             # {'name': '王大錘', 'height': 178}
person.clear()
print(person)             # {}
# === 範例 12 ===
person = {'name': '王大錘', 'age': 25, 'height': 178, 'addr': '成都市武侯區科華北路62號1棟101'}
del person['age']
del person['addr']
print(person)  # {'name': '王大錘', 'height': 178}
# === 範例 13 ===
sentence = input('請輸入一段話: ')
counter = {}
for ch in sentence:
    if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
        counter[ch] = counter.get(ch, 0) + 1
sorted_keys = sorted(counter, key=counter.get, reverse=True)
for key in sorted_keys:
    print(f'{key} 出現了 {counter[key]} 次.')
# === 範例 14 ===
stocks = {
    'AAPL': 191.88,
    'GOOG': 1186.96,
    'IBM': 149.24,
    'ORCL': 48.44,
    'ACN': 166.89,
    'FB': 208.09,
    'SYMC': 21.29
}
stocks2 = {key: value for key, value in stocks.items() if value > 100}
print(stocks2)
