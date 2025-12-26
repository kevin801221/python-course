"""
函式應用實戰 - 進階練習解答
============================
"""

import random
import string
import re
from collections import Counter

# ============================================================
# 練習 1：密碼生成器（基礎）
# ============================================================
print("=" * 40)
print("【練習 1：密碼生成器】")
print("=" * 40)


def generate_password(length=12, use_upper=True, use_digits=True, use_special=True):
    """生成隨機密碼"""
    chars = string.ascii_lowercase  # 小寫字母

    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*"

    password = ''.join(random.choice(chars) for _ in range(length))
    return password


print(f"generate_password() → {generate_password()}")
print(f"generate_password(8, use_special=False) → {generate_password(8, use_special=False)}")
print(f"generate_password(16) → {generate_password(16)}")


# ============================================================
# 練習 2：資料驗證函式（基礎）
# ============================================================
print()
print("=" * 40)
print("【練習 2：資料驗證函式】")
print("=" * 40)


def validate_email(email):
    """驗證電子郵件格式"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """驗證台灣手機號碼"""
    pattern = r'^09\d{8}$'
    return bool(re.match(pattern, phone))


def validate_password(password):
    """驗證密碼強度"""
    result = {
        'valid': False,
        'strength': '弱',
        'issues': []
    }

    # 檢查各項條件
    if len(password) < 8:
        result['issues'].append('長度至少 8 個字元')
    if not any(c.isupper() for c in password):
        result['issues'].append('需包含大寫字母')
    if not any(c.islower() for c in password):
        result['issues'].append('需包含小寫字母')
    if not any(c.isdigit() for c in password):
        result['issues'].append('需包含數字')
    if not any(c in '!@#$%^&*' for c in password):
        result['issues'].append('需包含特殊字元')

    # 計算強度
    score = 5 - len(result['issues'])
    if score == 5:
        result['strength'] = '強'
        result['valid'] = True
    elif score >= 3:
        result['strength'] = '中'
    else:
        result['strength'] = '弱'

    return result


print(f'validate_email("test@example.com") → {validate_email("test@example.com")}')
print(f'validate_phone("0912345678") → {validate_phone("0912345678")}')
print(f'validate_password("Abc123!@#") → {validate_password("Abc123!@#")}')


# ============================================================
# 練習 3：統計函式庫（進階）
# ============================================================
print()
print("=" * 40)
print("【練習 3：統計函式庫】")
print("=" * 40)


def mean(data):
    """計算平均值"""
    if not data:
        return 0
    return sum(data) / len(data)


def median(data):
    """計算中位數"""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]


def mode(data):
    """計算眾數"""
    if not data:
        return None
    counter = Counter(data)
    return counter.most_common(1)[0][0]


def variance(data):
    """計算變異數"""
    if not data:
        return 0
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data) / len(data)


def std_dev(data):
    """計算標準差"""
    return variance(data) ** 0.5


data = [1, 2, 2, 3, 4, 5]
print(f"data = {data}")
print(f"mean(data) → {mean(data):.2f}")
print(f"median(data) → {median(data)}")
print(f"mode(data) → {mode(data)}")
print(f"std_dev(data) → {std_dev(data):.2f}")
print(f"variance(data) → {variance(data):.2f}")


# ============================================================
# 練習 4：文字處理函式（挑戰）
# ============================================================
print()
print("=" * 40)
print("【練習 4：文字處理函式】")
print("=" * 40)


def word_count(text):
    """統計單字數量"""
    words = text.lower().split()
    # 移除標點符號
    words = [word.strip(string.punctuation) for word in words]
    return dict(Counter(words))


def char_frequency(text):
    """統計字元頻率"""
    # 只統計字母
    chars = [c.lower() for c in text if c.isalpha()]
    return dict(Counter(chars))


def reverse_words(text):
    """反轉每個單字"""
    words = text.split()
    reversed_words = [word[::-1] for word in words]
    return ' '.join(reversed_words)


def is_palindrome(text):
    """判斷是否為回文（忽略空格和大小寫）"""
    # 只保留字母，轉小寫
    cleaned = ''.join(c.lower() for c in text if c.isalpha())
    return cleaned == cleaned[::-1]


print(f'word_count("Hello world hello") → {word_count("Hello world hello")}')
print(f'char_frequency("Hello") → {char_frequency("Hello")}')
print(f'reverse_words("Hello World") → {reverse_words("Hello World")}')
print(f'is_palindrome("A man a plan a canal Panama") → {is_palindrome("A man a plan a canal Panama")}')
print(f'is_palindrome("race car") → {is_palindrome("race car")}')


# ============================================================
# 【函式設計原則】
# ============================================================
"""
【單一職責原則】
每個函式只做一件事

【函式命名】
- 使用動詞開頭：get_user, calculate_total, validate_email
- 使用 is_/has_ 開頭表示布林值：is_valid, has_permission

【參數設計】
- 參數不宜過多（建議 3 個以內）
- 使用預設參數減少必填參數
- 複雜參數考慮使用字典或物件

【文件字串】
def function(arg):
    '''
    簡短描述

    Args:
        arg: 參數說明

    Returns:
        返回值說明

    Raises:
        可能拋出的異常
    '''
    pass
"""
