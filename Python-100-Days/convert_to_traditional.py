#!/usr/bin/env python3
"""
轉換腳本：將所有 .md 檔案從簡體中文轉成繁體中文，並提取 Python 代碼生成 .py 檔
"""

import os
import re
from pathlib import Path
from opencc import OpenCC

# 初始化 OpenCC 轉換器 (簡體轉繁體台灣標準)
cc = OpenCC('s2twp')


def convert_file_to_traditional(file_path: Path) -> None:
    """將單一檔案轉換成繁體中文"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 轉換成繁體中文
        traditional_content = cc.convert(content)

        # 寫回原檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(traditional_content)

        print(f"已轉換: {file_path}")
    except Exception as e:
        print(f"轉換失敗 {file_path}: {e}")


def extract_python_code(md_file_path: Path) -> None:
    """從 markdown 檔案提取 Python 代碼並生成 .py 檔"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 找出所有 Python 代碼區塊
        pattern = r'```python\s*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            return

        # 生成 .py 檔案名稱
        py_file_name = md_file_path.stem + '.py'
        py_file_path = md_file_path.parent / py_file_name

        # 合併所有 Python 代碼區塊
        code_blocks = []
        for i, code in enumerate(matches, 1):
            code = code.strip()
            if code:
                code_blocks.append(f"# === 範例 {i} ===\n{code}")

        if code_blocks:
            full_code = f'''#!/usr/bin/env python3
"""
從 {md_file_path.name} 提取的 Python 範例代碼
"""

{chr(10).join(code_blocks)}
'''
            with open(py_file_path, 'w', encoding='utf-8') as f:
                f.write(full_code)

            print(f"已生成: {py_file_path}")
    except Exception as e:
        print(f"提取代碼失敗 {md_file_path}: {e}")


def main():
    """主程序"""
    base_dir = Path(__file__).parent

    # 找出所有 .md 檔案
    md_files = list(base_dir.rglob('*.md'))
    print(f"找到 {len(md_files)} 個 markdown 檔案\n")

    print("=" * 50)
    print("步驟 1: 轉換成繁體中文")
    print("=" * 50)

    for md_file in md_files:
        # 跳過 .git 目錄
        if '.git' in str(md_file):
            continue
        convert_file_to_traditional(md_file)

    print("\n" + "=" * 50)
    print("步驟 2: 提取 Python 代碼")
    print("=" * 50)

    for md_file in md_files:
        # 跳過 .git 目錄
        if '.git' in str(md_file):
            continue
        extract_python_code(md_file)

    print("\n完成!")


if __name__ == '__main__':
    main()
