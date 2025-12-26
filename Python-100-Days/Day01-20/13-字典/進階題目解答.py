"""
字典 - 進階練習解答
====================
"""

# ============================================================
# 練習 1：字典基本操作（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：字典基本操作】")
print("=" * 40)

# 建立字典
student = {
    'name': 'Alice',
    'age': 18,
    'score': 95
}

print(f"學生資料：{student}")
print(f"姓名：{student['name']}")
print(f"年齡：{student['age']}")
print(f"成績：{student['score']}")

# 新增資料
student['class'] = '高三甲'
print(f"\n新增班級後：{student}")

# 修改資料
student['score'] = 98
print(f"修改成績後：{student}")

# 刪除資料
del student['class']
print(f"刪除班級後：{student}")

# 遍歷字典
print("\n遍歷字典：")
for key, value in student.items():
    print(f"  {key}: {value}")


# ============================================================
# 練習 2：單字統計（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：單字統計】")
print("=" * 40)

text = input("請輸入文字：")
words = text.lower().split()

# 統計單字
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

# 按次數排序
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

print("\n【單字統計】")
for word, count in sorted_words:
    print(f"{word}: {count} 次")


# ============================================================
# 練習 3：成績管理系統（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：成績管理系統】")
print("=" * 40)

students = {}

while True:
    print("\n【成績管理系統】")
    print("1. 新增學生")
    print("2. 新增成績")
    print("3. 查詢成績")
    print("4. 班級排名")
    print("0. 退出")

    choice = input("\n請選擇：")

    if choice == "1":
        name = input("請輸入學生姓名：")
        if name not in students:
            students[name] = {}
            print(f"已新增學生：{name}")
        else:
            print("學生已存在！")

    elif choice == "2":
        if not students:
            print("尚無學生資料！")
            continue
        name = input("請輸入學生姓名：")
        if name in students:
            subject = input("請輸入科目：")
            score = float(input("請輸入成績："))
            students[name][subject] = score
            print(f"已記錄 {name} 的 {subject} 成績：{score}")
        else:
            print("找不到該學生！")

    elif choice == "3":
        if not students:
            print("尚無學生資料！")
            continue
        name = input("請輸入學生姓名：")
        if name in students:
            print(f"\n【{name} 的成績】")
            scores = students[name]
            if scores:
                for subject, score in scores.items():
                    print(f"  {subject}: {score}")
                avg = sum(scores.values()) / len(scores)
                print(f"  平均：{avg:.2f}")
            else:
                print("  尚無成績記錄")
        else:
            print("找不到該學生！")

    elif choice == "4":
        if not students:
            print("尚無學生資料！")
            continue

        # 計算每位學生的平均分
        rankings = []
        for name, scores in students.items():
            if scores:
                avg = sum(scores.values()) / len(scores)
                rankings.append((name, avg))

        if rankings:
            rankings.sort(key=lambda x: x[1], reverse=True)
            print("\n【班級排名】")
            for rank, (name, avg) in enumerate(rankings, 1):
                print(f"  {rank}. {name}: {avg:.2f}")
        else:
            print("尚無成績記錄！")

    elif choice == "0":
        print("再見！")
        break


# ============================================================
# 練習 4：購物車系統（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：購物車系統】")
print("=" * 40)

# 商品目錄
products = {
    '1': {'name': '蘋果', 'price': 30, 'stock': 50},
    '2': {'name': '香蕉', 'price': 20, 'stock': 30},
    '3': {'name': '橘子', 'price': 25, 'stock': 40},
    '4': {'name': '葡萄', 'price': 60, 'stock': 20},
}

cart = {}

while True:
    print("\n【購物系統】")
    print("1. 查看商品")
    print("2. 加入購物車")
    print("3. 查看購物車")
    print("4. 結帳")
    print("0. 退出")

    choice = input("\n請選擇：")

    if choice == "1":
        print("\n【商品目錄】")
        for pid, info in products.items():
            print(f"{pid}. {info['name']} - ${info['price']}/個 (庫存: {info['stock']})")

    elif choice == "2":
        print("\n【商品目錄】")
        for pid, info in products.items():
            print(f"{pid}. {info['name']} - ${info['price']}")

        pid = input("\n請輸入商品編號：")
        if pid in products:
            try:
                qty = int(input("請輸入數量："))
                if qty > 0 and qty <= products[pid]['stock']:
                    product_name = products[pid]['name']
                    if product_name in cart:
                        cart[product_name] += qty
                    else:
                        cart[product_name] = qty
                    print(f"已加入：{product_name} x {qty}")
                else:
                    print("數量無效或超過庫存！")
            except ValueError:
                print("請輸入有效數字！")
        else:
            print("商品不存在！")

    elif choice == "3":
        if cart:
            print("\n【購物車】")
            total = 0
            for product_name, qty in cart.items():
                # 找到價格
                for info in products.values():
                    if info['name'] == product_name:
                        subtotal = info['price'] * qty
                        total += subtotal
                        print(f"{product_name} x {qty} = ${subtotal}")
                        break
            print("-" * 20)
            print(f"總計：${total}")
        else:
            print("\n購物車是空的。")

    elif choice == "4":
        if cart:
            print("\n【結帳明細】")
            total = 0
            for product_name, qty in cart.items():
                for info in products.values():
                    if info['name'] == product_name:
                        subtotal = info['price'] * qty
                        total += subtotal
                        print(f"{product_name} x {qty} = ${subtotal}")
                        break
            print("-" * 20)
            print(f"總計：${total}")
            print("\n感謝購買！")
            cart.clear()
        else:
            print("\n購物車是空的。")

    elif choice == "0":
        print("感謝光臨！")
        break


# ============================================================
# 【字典方法整理】
# ============================================================
"""
【建立字典】
dict()          空字典
{'a': 1}        字面量
dict(a=1)       關鍵字參數
dict([('a',1)]) 從序列建立

【存取】
d[key]          取值（不存在會報錯）
d.get(key)      取值（不存在返回 None）
d.get(key, default) 取值（不存在返回預設值）

【新增/修改】
d[key] = value  設定值
d.update(dict2) 合併字典
d.setdefault()  不存在時設定預設值

【刪除】
del d[key]      刪除鍵值對
d.pop(key)      刪除並返回值
d.clear()       清空字典

【遍歷】
d.keys()        所有鍵
d.values()      所有值
d.items()       所有鍵值對

【其他】
len(d)          字典長度
key in d        檢查鍵是否存在
"""
