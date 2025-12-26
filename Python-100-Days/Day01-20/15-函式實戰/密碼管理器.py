"""
密碼管理器 - Password Manager
==============================
進階應用：展示 Python 函式的實戰應用

功能：
1. 密碼生成（多種規則）
2. 密碼強度檢測
3. 密碼加密儲存
4. 函式作為參數
"""

import random
import string
import hashlib
import json
import os
from typing import Callable, Optional
from datetime import datetime


# ========================================
# 1. 密碼生成函式
# ========================================

def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    exclude_chars: str = ""
) -> str:
    """
    生成隨機密碼

    Args:
        length: 密碼長度
        use_uppercase: 包含大寫字母
        use_lowercase: 包含小寫字母
        use_digits: 包含數字
        use_special: 包含特殊字元
        exclude_chars: 排除的字元

    Returns:
        生成的密碼
    """
    chars = ""

    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # 移除排除字元
    for c in exclude_chars:
        chars = chars.replace(c, "")

    if not chars:
        raise ValueError("至少需要選擇一種字元類型")

    return ''.join(random.choice(chars) for _ in range(length))


def generate_memorable_password(words: int = 4, separator: str = "-") -> str:
    """生成易記密碼（使用隨機單字）"""
    word_list = [
        "apple", "banana", "cherry", "dragon", "eagle", "falcon",
        "galaxy", "happy", "island", "jungle", "kitten", "lemon",
        "mango", "night", "ocean", "piano", "queen", "river",
        "sunset", "tiger", "urban", "violet", "winter", "yellow",
        "zebra", "alpha", "brave", "cloud", "delta", "ember"
    ]
    selected = random.sample(word_list, min(words, len(word_list)))
    # 隨機替換一些字母為數字
    result = separator.join(selected)
    replacements = {'a': '4', 'e': '3', 'i': '1', 'o': '0'}
    for old, new in replacements.items():
        if random.random() > 0.5:
            result = result.replace(old, new, 1)
    return result + str(random.randint(10, 99))


def generate_pin(length: int = 6) -> str:
    """生成數字 PIN 碼"""
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_pattern_password(pattern: str) -> str:
    """
    依照模式生成密碼

    模式說明：
    - A: 大寫字母
    - a: 小寫字母
    - 9: 數字
    - #: 特殊字元
    - 其他: 原樣保留
    """
    result = []
    for char in pattern:
        if char == 'A':
            result.append(random.choice(string.ascii_uppercase))
        elif char == 'a':
            result.append(random.choice(string.ascii_lowercase))
        elif char == '9':
            result.append(random.choice(string.digits))
        elif char == '#':
            result.append(random.choice("!@#$%^&*"))
        else:
            result.append(char)
    return ''.join(result)


# ========================================
# 2. 密碼強度檢測函式
# ========================================

def check_password_strength(password: str) -> dict:
    """
    檢測密碼強度

    Returns:
        包含強度分數和詳細評估的字典
    """
    score = 0
    feedback = []

    # 長度檢查
    if len(password) >= 16:
        score += 2
        feedback.append("✅ 長度優秀 (16+)")
    elif len(password) >= 12:
        score += 1
        feedback.append("✅ 長度良好 (12+)")
    elif len(password) >= 8:
        score += 0.5
        feedback.append("⚠️ 長度尚可 (8+)")
    else:
        feedback.append("❌ 密碼太短 (<8)")

    # 字元類型檢查
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_upper:
        score += 1
        feedback.append("✅ 包含大寫字母")
    else:
        feedback.append("❌ 缺少大寫字母")

    if has_lower:
        score += 1
        feedback.append("✅ 包含小寫字母")
    else:
        feedback.append("❌ 缺少小寫字母")

    if has_digit:
        score += 1
        feedback.append("✅ 包含數字")
    else:
        feedback.append("❌ 缺少數字")

    if has_special:
        score += 1
        feedback.append("✅ 包含特殊字元")
    else:
        feedback.append("❌ 缺少特殊字元")

    # 常見模式檢查
    common_patterns = ['123', 'abc', 'qwerty', 'password', '111', 'aaa']
    for pattern in common_patterns:
        if pattern.lower() in password.lower():
            score -= 1
            feedback.append(f"⚠️ 包含常見模式: {pattern}")

    # 連續字元檢查
    consecutive = 0
    for i in range(1, len(password)):
        if password[i] == password[i-1]:
            consecutive += 1
    if consecutive >= 3:
        score -= 0.5
        feedback.append("⚠️ 有連續重複字元")

    # 計算等級
    if score >= 6:
        level = "強"
        level_icon = "🟢"
    elif score >= 4:
        level = "中"
        level_icon = "🟡"
    elif score >= 2:
        level = "弱"
        level_icon = "🟠"
    else:
        level = "非常弱"
        level_icon = "🔴"

    return {
        'password': password,
        'score': max(0, score),
        'max_score': 7,
        'level': level,
        'level_icon': level_icon,
        'feedback': feedback,
    }


# ========================================
# 3. 密碼加密函式
# ========================================

def hash_password(password: str, salt: str = "") -> str:
    """使用 SHA-256 雜湊密碼"""
    salted = salt + password + salt
    return hashlib.sha256(salted.encode()).hexdigest()


def generate_salt(length: int = 16) -> str:
    """生成隨機鹽值"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def verify_password(password: str, hashed: str, salt: str = "") -> bool:
    """驗證密碼"""
    return hash_password(password, salt) == hashed


def simple_encrypt(text: str, key: int = 7) -> str:
    """簡單加密（Caesar cipher 變體）"""
    result = []
    for char in text:
        result.append(chr(ord(char) + key))
    return ''.join(result)


def simple_decrypt(text: str, key: int = 7) -> str:
    """簡單解密"""
    result = []
    for char in text:
        result.append(chr(ord(char) - key))
    return ''.join(result)


# ========================================
# 4. 密碼管理器類別
# ========================================

class PasswordManager:
    """密碼管理器"""

    def __init__(self, master_password: str):
        self.master_hash = hash_password(master_password, "master_salt")
        self.vault = {}  # {網站: {username, encrypted_password, salt, created_at}}
        self.encryption_key = sum(ord(c) for c in master_password) % 20 + 1

    def verify_master(self, password: str) -> bool:
        """驗證主密碼"""
        return hash_password(password, "master_salt") == self.master_hash

    def add_entry(self, site: str, username: str, password: str):
        """新增密碼條目"""
        salt = generate_salt()
        encrypted = simple_encrypt(password, self.encryption_key)

        self.vault[site] = {
            'username': username,
            'encrypted_password': encrypted,
            'salt': salt,
            'password_hash': hash_password(password, salt),
            'created_at': datetime.now().isoformat(),
        }

    def get_entry(self, site: str) -> Optional[dict]:
        """取得密碼條目"""
        if site in self.vault:
            entry = self.vault[site].copy()
            entry['password'] = simple_decrypt(
                entry['encrypted_password'],
                self.encryption_key
            )
            return entry
        return None

    def list_sites(self) -> list:
        """列出所有網站"""
        return list(self.vault.keys())

    def delete_entry(self, site: str) -> bool:
        """刪除條目"""
        if site in self.vault:
            del self.vault[site]
            return True
        return False

    def export_vault(self, filename: str):
        """匯出保險庫（不含解密密碼）"""
        export_data = {}
        for site, data in self.vault.items():
            export_data[site] = {
                'username': data['username'],
                'created_at': data['created_at'],
            }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


# ========================================
# 5. 批次操作函式
# ========================================

def batch_generate(
    count: int,
    generator: Callable[[], str] = lambda: generate_password()
) -> list:
    """批次生成密碼（函式作為參數）"""
    return [generator() for _ in range(count)]


def filter_passwords(
    passwords: list,
    condition: Callable[[str], bool]
) -> list:
    """過濾密碼（條件函式）"""
    return [p for p in passwords if condition(p)]


# ========================================
# 主程式
# ========================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║              密碼管理器 v1.0                           ║
║           展示 Python 函式實戰應用                     ║
╚══════════════════════════════════════════════════════╝
    """)

    # 設定主密碼
    master = input("設定主密碼: ").strip() or "demo123"
    manager = PasswordManager(master)
    print("✅ 密碼管理器已初始化！")

    while True:
        print("""
【選單】
  1. 生成密碼        2. 檢測強度
  3. 儲存密碼        4. 查看密碼
  5. 批次生成        6. 密碼加密展示
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n🔑 密碼生成")
            print("=" * 50)
            print("""
  1. 隨機密碼（自訂規則）
  2. 易記密碼（單字組合）
  3. PIN 碼
  4. 模式密碼
""")
            sub = input("選擇: ").strip()

            if sub == '1':
                try:
                    length = int(input("長度 (預設16): ") or "16")
                    upper = input("含大寫? (Y/n): ").lower() != 'n'
                    lower = input("含小寫? (Y/n): ").lower() != 'n'
                    digits = input("含數字? (Y/n): ").lower() != 'n'
                    special = input("含特殊? (Y/n): ").lower() != 'n'

                    password = generate_password(
                        length=length,
                        use_uppercase=upper,
                        use_lowercase=lower,
                        use_digits=digits,
                        use_special=special
                    )
                    print(f"\n生成的密碼: {password}")

                except Exception as e:
                    print(f"❌ 錯誤: {e}")

            elif sub == '2':
                words = int(input("單字數量 (預設4): ") or "4")
                password = generate_memorable_password(words)
                print(f"\n易記密碼: {password}")

            elif sub == '3':
                length = int(input("PIN 長度 (預設6): ") or "6")
                password = generate_pin(length)
                print(f"\nPIN 碼: {password}")

            elif sub == '4':
                print("模式說明: A=大寫 a=小寫 9=數字 #=特殊")
                pattern = input("輸入模式 (如 Aaaa-9999-#): ") or "Aaaa-9999-##"
                password = generate_pattern_password(pattern)
                print(f"\n模式密碼: {password}")

        elif choice == '2':
            print("\n🔍 密碼強度檢測")
            print("=" * 50)

            password = input("輸入要檢測的密碼: ").strip()
            if not password:
                password = "Test123!"
                print(f"使用範例密碼: {password}")

            result = check_password_strength(password)

            print(f"\n密碼: {'*' * len(password)}")
            print(f"長度: {len(password)}")
            print(f"強度: {result['level_icon']} {result['level']}")
            print(f"分數: {result['score']:.1f} / {result['max_score']}")
            print("\n詳細評估:")
            for fb in result['feedback']:
                print(f"  {fb}")

        elif choice == '3':
            print("\n💾 儲存密碼")
            print("=" * 50)

            site = input("網站/服務名稱: ").strip()
            if not site:
                print("❌ 網站名稱不能為空")
                continue

            username = input("使用者名稱: ").strip()

            gen_new = input("是否生成新密碼? (Y/n): ").lower() != 'n'
            if gen_new:
                password = generate_password()
                print(f"生成的密碼: {password}")
            else:
                password = input("輸入密碼: ").strip()

            manager.add_entry(site, username, password)
            print(f"✅ 已儲存 {site} 的密碼！")

        elif choice == '4':
            print("\n📋 查看密碼")
            print("=" * 50)

            sites = manager.list_sites()
            if not sites:
                print("(尚無儲存的密碼)")
                continue

            print("已儲存的網站:")
            for i, site in enumerate(sites, 1):
                print(f"  {i}. {site}")

            site_input = input("\n輸入網站名稱或編號: ").strip()

            # 支援編號選擇
            if site_input.isdigit():
                idx = int(site_input) - 1
                if 0 <= idx < len(sites):
                    site_input = sites[idx]

            # 驗證主密碼
            verify = input("輸入主密碼確認: ").strip()
            if not manager.verify_master(verify):
                print("❌ 主密碼錯誤！")
                continue

            entry = manager.get_entry(site_input)
            if entry:
                print(f"\n網站: {site_input}")
                print(f"使用者: {entry['username']}")
                print(f"密碼: {entry['password']}")
                print(f"建立: {entry['created_at']}")
            else:
                print("❌ 找不到該網站！")

        elif choice == '5':
            print("\n📦 批次生成")
            print("=" * 50)

            count = int(input("生成數量 (預設5): ") or "5")

            # 使用函式作為參數
            passwords = batch_generate(count, lambda: generate_password(12))

            print(f"\n生成的 {count} 個密碼:")
            for i, pwd in enumerate(passwords, 1):
                strength = check_password_strength(pwd)
                print(f"  {i}. {pwd}  {strength['level_icon']}")

            # 過濾強密碼
            strong = filter_passwords(
                passwords,
                lambda p: check_password_strength(p)['score'] >= 5
            )
            print(f"\n其中強度足夠的有 {len(strong)} 個")

        elif choice == '6':
            print("\n🔐 密碼加密展示")
            print("=" * 50)

            password = input("輸入測試密碼: ") or "MySecret123"

            # 雜湊
            salt = generate_salt()
            hashed = hash_password(password, salt)
            print(f"\n原始密碼: {password}")
            print(f"鹽值: {salt}")
            print(f"SHA-256 雜湊: {hashed[:32]}...")

            # 驗證
            test = input("\n輸入密碼驗證: ").strip()
            if verify_password(test, hashed, salt):
                print("✅ 密碼正確！")
            else:
                print("❌ 密碼錯誤！")

            # 簡單加密
            encrypted = simple_encrypt(password, 5)
            decrypted = simple_decrypt(encrypted, 5)
            print(f"\n簡單加密: {encrypted}")
            print(f"解密還原: {decrypted}")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
