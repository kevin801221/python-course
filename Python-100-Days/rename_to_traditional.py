#!/usr/bin/env python3
"""
重命名腳本：將所有檔案和資料夾名稱從簡體中文轉成繁體中文
"""

import os
from pathlib import Path
from opencc import OpenCC

# 初始化 OpenCC 轉換器 (簡體轉繁體台灣標準)
cc = OpenCC('s2twp')


def get_all_paths(base_dir: Path) -> list[Path]:
    """取得所有檔案和資料夾路徑，按深度排序（最深的優先）"""
    all_paths = []

    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)

        # 跳過 .git 目錄
        if '.git' in str(root_path):
            continue

        # 加入檔案
        for file in files:
            file_path = root_path / file
            all_paths.append(file_path)

        # 加入資料夾
        for dir_name in dirs:
            if dir_name == '.git':
                continue
            dir_path = root_path / dir_name
            all_paths.append(dir_path)

    # 按路徑深度排序，最深的優先（這樣重命名時不會影響父路徑）
    all_paths.sort(key=lambda p: len(p.parts), reverse=True)

    return all_paths


def needs_conversion(text: str) -> bool:
    """檢查文字是否需要轉換（包含簡體中文字符）"""
    converted = cc.convert(text)
    return converted != text


def rename_path(path: Path) -> Path | None:
    """重命名單一路徑，回傳新路徑或 None（如果不需要轉換）"""
    name = path.name
    new_name = cc.convert(name)

    if new_name == name:
        return None

    new_path = path.parent / new_name

    try:
        path.rename(new_path)
        print(f"重命名: {name} -> {new_name}")
        return new_path
    except Exception as e:
        print(f"重命名失敗 {path}: {e}")
        return None


def main():
    """主程序"""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("開始將檔案和資料夾名稱從簡體中文轉換為繁體中文")
    print("=" * 60)
    print()

    # 取得所有路徑
    all_paths = get_all_paths(base_dir)
    print(f"找到 {len(all_paths)} 個檔案和資料夾\n")

    # 統計
    renamed_count = 0
    skipped_count = 0

    for path in all_paths:
        # 跳過此腳本自己
        if path.name in ('rename_to_traditional.py', 'convert_to_traditional.py'):
            continue

        if path.exists():
            result = rename_path(path)
            if result:
                renamed_count += 1
            else:
                skipped_count += 1

    print()
    print("=" * 60)
    print(f"完成！已重命名 {renamed_count} 個檔案/資料夾")
    print(f"跳過 {skipped_count} 個（無需轉換）")
    print("=" * 60)


if __name__ == '__main__':
    main()
