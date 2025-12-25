#!/usr/bin/env python3
"""
從 22.对象的序列化和反序列化.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import json

my_dict = {
    'name': 'Kevin',
    'age': 40,
    'friends': ['王大錘', '白元芳'],
    'cars': [
        {'brand': 'BMW', 'max_speed': 240},
        {'brand': 'Audi', 'max_speed': 280},
        {'brand': 'Benz', 'max_speed': 280}
    ]
}
print(json.dumps(my_dict))
# === 範例 2 ===
import json

my_dict = {
    'name': 'Kevin',
    'age': 40,
    'friends': ['王大錘', '白元芳'],
    'cars': [
        {'brand': 'BMW', 'max_speed': 240},
        {'brand': 'Audi', 'max_speed': 280},
        {'brand': 'Benz', 'max_speed': 280}
    ]
}
with open('data.json', 'w') as file:
    json.dump(my_dict, file)
# === 範例 3 ===
import json

with open('data.json', 'r') as file:
    my_dict = json.load(file)
    print(type(my_dict))
    print(my_dict)
# === 範例 4 ===
import requests

resp = requests.get('http://api.tianapi.com/guonei/?key=APIKey&num=10')
if resp.status_code == 200:
    data_model = resp.json()
    for news in data_model['newslist']:
        print(news['title'])
        print(news['url'])
        print('-' * 60)
