"""
文字處理工具箱 - Text Processing Toolkit
========================================
進階應用：展示 Python 字串的各種操作

功能：
1. 文字統計分析
2. 格式轉換
3. 文字加密解密
4. 模板引擎
"""

import re
from collections import Counter


class TextAnalyzer:
    """文字分析器"""

    def __init__(self, text: str):
        self.text = text

    def count_chars(self):
        """字元統計"""
        return {
            '總字元': len(self.text),
            '不含空白': len(self.text.replace(' ', '')),
            '字母': sum(c.isalpha() for c in self.text),
            '數字': sum(c.isdigit() for c in self.text),
            '空白': sum(c.isspace() for c in self.text),
            '標點': sum(not c.isalnum() and not c.isspace() for c in self.text),
        }

    def count_words(self):
        """單字統計"""
        words = self.text.split()
        return len(words)

    def count_lines(self):
        """行數統計"""
        return len(self.text.splitlines()) or 1

    def word_frequency(self, top_n=10):
        """詞頻統計"""
        # 移除標點並轉小寫
        clean = re.sub(r'[^\w\s]', '', self.text.lower())
        words = clean.split()
        return Counter(words).most_common(top_n)

    def find_pattern(self, pattern):
        """正則表達式搜尋"""
        return re.findall(pattern, self.text)

    def find_emails(self):
        """找出所有電子郵件"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return self.find_pattern(pattern)

    def find_urls(self):
        """找出所有網址"""
        pattern = r'https?://[^\s]+'
        return self.find_pattern(pattern)

    def find_phones(self):
        """找出電話號碼"""
        pattern = r'\d{4}[-.]?\d{3}[-.]?\d{3}'
        return self.find_pattern(pattern)


class TextFormatter:
    """文字格式化器"""

    @staticmethod
    def to_title_case(text: str) -> str:
        """首字母大寫"""
        return text.title()

    @staticmethod
    def to_upper(text: str) -> str:
        """全部大寫"""
        return text.upper()

    @staticmethod
    def to_lower(text: str) -> str:
        """全部小寫"""
        return text.lower()

    @staticmethod
    def to_snake_case(text: str) -> str:
        """轉換為 snake_case"""
        # 將空格和連字號轉換為底線
        text = re.sub(r'[\s-]+', '_', text)
        # 在大寫字母前加底線
        text = re.sub(r'([A-Z])', r'_\1', text)
        return text.lower().strip('_')

    @staticmethod
    def to_camel_case(text: str) -> str:
        """轉換為 camelCase"""
        words = re.split(r'[\s_-]+', text)
        return words[0].lower() + ''.join(w.title() for w in words[1:])

    @staticmethod
    def to_pascal_case(text: str) -> str:
        """轉換為 PascalCase"""
        words = re.split(r'[\s_-]+', text)
        return ''.join(w.title() for w in words)

    @staticmethod
    def reverse(text: str) -> str:
        """反轉字串"""
        return text[::-1]

    @staticmethod
    def center_text(text: str, width: int = 50, char: str = '-') -> str:
        """置中文字"""
        return text.center(width, char)

    @staticmethod
    def wrap_text(text: str, width: int = 40) -> str:
        """自動換行"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + len(current_line) <= width:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)


class TextCrypto:
    """簡單加密解密"""

    @staticmethod
    def caesar_encrypt(text: str, shift: int = 3) -> str:
        """凱薩加密"""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + shift) % 26 + base
                result.append(chr(shifted))
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def caesar_decrypt(text: str, shift: int = 3) -> str:
        """凱薩解密"""
        return TextCrypto.caesar_encrypt(text, -shift)

    @staticmethod
    def morse_encode(text: str) -> str:
        """摩斯密碼編碼"""
        morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.', ' ': '/'
        }
        return ' '.join(morse_code.get(c.upper(), c) for c in text)

    @staticmethod
    def rot13(text: str) -> str:
        """ROT13 編碼（加解密相同）"""
        return TextCrypto.caesar_encrypt(text, 13)


class TemplateEngine:
    """簡單模板引擎"""

    def __init__(self, template: str):
        self.template = template

    def render(self, **kwargs) -> str:
        """渲染模板"""
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f'{{{{{key}}}}}', str(value))
        return result


def main():
    print("""
╔══════════════════════════════════════════════════════╗
║            文字處理工具箱 v1.0                         ║
║           展示 Python 字串操作                         ║
╚══════════════════════════════════════════════════════╝
    """)

    sample_text = """Hello World! This is a sample text.
It contains multiple lines and various words.
Contact us at support@example.com or visit https://example.com
Phone: 0912-345-678"""

    while True:
        print("""
【選單】
  1. 文字統計分析    2. 格式轉換
  3. 加密解密        4. 模板引擎
  5. 輸入自訂文字    0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n📊 文字統計分析")
            print("=" * 50)
            text = input("輸入文字 (留空用範例): ").strip() or sample_text
            print(f"\n文字內容:\n{text[:200]}{'...' if len(text) > 200 else ''}")

            analyzer = TextAnalyzer(text)

            print("\n📈 基本統計:")
            for key, value in analyzer.count_chars().items():
                print(f"  {key}: {value}")

            print(f"\n  單字數: {analyzer.count_words()}")
            print(f"  行數: {analyzer.count_lines()}")

            print("\n📊 詞頻統計 (前10):")
            for word, count in analyzer.word_frequency(10):
                bar = "█" * count
                print(f"  {word:15} {bar} ({count})")

            emails = analyzer.find_emails()
            urls = analyzer.find_urls()
            phones = analyzer.find_phones()

            if emails:
                print(f"\n📧 找到的Email: {', '.join(emails)}")
            if urls:
                print(f"🔗 找到的網址: {', '.join(urls)}")
            if phones:
                print(f"📱 找到的電話: {', '.join(phones)}")

        elif choice == '2':
            print("\n✏️ 格式轉換")
            print("=" * 50)
            text = input("輸入文字: ").strip() or "hello world example"

            print(f"\n原始: {text}")
            print(f"首字母大寫: {TextFormatter.to_title_case(text)}")
            print(f"全部大寫: {TextFormatter.to_upper(text)}")
            print(f"全部小寫: {TextFormatter.to_lower(text)}")
            print(f"snake_case: {TextFormatter.to_snake_case(text)}")
            print(f"camelCase: {TextFormatter.to_camel_case(text)}")
            print(f"PascalCase: {TextFormatter.to_pascal_case(text)}")
            print(f"反轉: {TextFormatter.reverse(text)}")
            print(f"\n置中:\n{TextFormatter.center_text(text, 50, '-')}")

        elif choice == '3':
            print("\n🔐 加密解密")
            print("=" * 50)
            text = input("輸入文字: ").strip() or "Hello World"

            print(f"\n原始: {text}")

            # 凱薩加密
            encrypted = TextCrypto.caesar_encrypt(text, 3)
            decrypted = TextCrypto.caesar_decrypt(encrypted, 3)
            print(f"\n凱薩加密 (shift=3): {encrypted}")
            print(f"凱薩解密: {decrypted}")

            # ROT13
            rot13 = TextCrypto.rot13(text)
            print(f"\nROT13: {rot13}")
            print(f"ROT13 還原: {TextCrypto.rot13(rot13)}")

            # 摩斯密碼
            morse = TextCrypto.morse_encode(text)
            print(f"\n摩斯密碼: {morse}")

        elif choice == '4':
            print("\n📝 模板引擎")
            print("=" * 50)

            template = """
親愛的 {{name}}：

感謝您於 {{date}} 購買了 {{product}}！
訂單金額: ${{amount}}
預計 {{days}} 天內送達。

{{company}} 敬上
"""
            print("模板內容:")
            print(template)

            print("\n填入資料:")
            engine = TemplateEngine(template)
            result = engine.render(
                name=input("姓名: ") or "王小明",
                date=input("日期: ") or "2024-01-15",
                product=input("商品: ") or "無線藍牙耳機",
                amount=input("金額: ") or "1,299",
                days=input("天數: ") or "3",
                company=input("公司: ") or "ABC 購物"
            )

            print("\n渲染結果:")
            print(result)

        elif choice == '5':
            sample_text = input("請輸入新的文字:\n")
            print("✅ 已更新範例文字！")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
