#!/usr/bin/env python3
"""
從 23.Python读写CSV文件.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import csv
import random

with open('scores.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['姓名', '語文', '數學', '英語'])
    names = ['關羽', '張飛', '趙雲', '馬超', '黃忠']
    for name in names:
        scores = [random.randrange(50, 101) for _ in range(3)]
        scores.insert(0, name)
        writer.writerow(scores)
# === 範例 2 ===
writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_ALL)
# === 範例 3 ===
import csv

with open('scores.csv', 'r') as file:
    reader = csv.reader(file, delimiter='|')
    for data_list in reader:
        print(reader.line_num, end='\t')
        for elem in data_list:
            print(elem, end='\t')
        print()
