"""
數字猜謎遊戲 - Number Guessing Game
===================================
進階應用：展示 Python 迴圈結構的互動式應用

功能：
1. 多種難度模式
2. 提示系統
3. 統計分析
4. 排行榜
"""

import random
from datetime import datetime


class GameStats:
    """遊戲統計"""

    def __init__(self):
        self.games_played = 0
        self.total_attempts = 0
        self.wins = 0
        self.best_score = float('inf')
        self.history = []

    def record_game(self, attempts, won, difficulty):
        self.games_played += 1
        self.total_attempts += attempts
        if won:
            self.wins += 1
            if attempts < self.best_score:
                self.best_score = attempts
        self.history.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'attempts': attempts,
            'won': won,
            'difficulty': difficulty
        })

    def show_stats(self):
        if self.games_played == 0:
            print("\n📊 還沒有遊戲記錄！")
            return

        avg = self.total_attempts / self.games_played
        win_rate = self.wins / self.games_played * 100

        print(f"""
╔══════════════════════════════════════╗
║            遊戲統計                   ║
╠══════════════════════════════════════╣
║  遊戲次數: {self.games_played:>5} 次                 ║
║  獲勝次數: {self.wins:>5} 次                 ║
║  勝率:     {win_rate:>5.1f}%                 ║
║  平均嘗試: {avg:>5.1f} 次                 ║
║  最佳成績: {self.best_score if self.best_score != float('inf') else '-':>5} 次                 ║
╚══════════════════════════════════════╝
""")

        print("\n📜 最近遊戲記錄:")
        for i, game in enumerate(self.history[-5:], 1):
            status = "✅" if game['won'] else "❌"
            print(f"  {i}. [{game['time']}] {game['difficulty']} - {game['attempts']}次 {status}")


def get_difficulty():
    """選擇難度"""
    print("""
╔══════════════════════════════════════╗
║           選擇難度                    ║
╠══════════════════════════════════════╣
║  1. 簡單 (1-50, 無限次數)            ║
║  2. 普通 (1-100, 10次機會)           ║
║  3. 困難 (1-500, 15次機會)           ║
║  4. 地獄 (1-1000, 10次機會)          ║
╚══════════════════════════════════════╝
""")

    difficulties = {
        '1': ('簡單', 1, 50, float('inf')),
        '2': ('普通', 1, 100, 10),
        '3': ('困難', 1, 500, 15),
        '4': ('地獄', 1, 1000, 10),
    }

    while True:
        choice = input("選擇難度 (1-4): ").strip()
        if choice in difficulties:
            return difficulties[choice]
        print("請輸入有效選項！")


def play_game(difficulty_info):
    """進行遊戲"""
    name, min_num, max_num, max_attempts = difficulty_info
    secret = random.randint(min_num, max_num)
    attempts = 0
    guesses = []

    print(f"""
🎮 【{name}模式】

我想了一個 {min_num} 到 {max_num} 之間的數字。
{'你有無限次機會！' if max_attempts == float('inf') else f'你有 {max_attempts} 次機會！'}
開始猜吧！

提示：輸入 'h' 查看歷史猜測, 'q' 放棄
""")

    # 使用 while 迴圈
    while attempts < max_attempts:
        remaining = max_attempts - attempts if max_attempts != float('inf') else '∞'
        guess_input = input(f"\n[剩餘 {remaining} 次] 請猜一個數字: ").strip().lower()

        # 特殊指令
        if guess_input == 'h':
            if guesses:
                print(f"歷史猜測: {', '.join(map(str, guesses))}")
            else:
                print("還沒有猜測記錄")
            continue

        if guess_input == 'q':
            print(f"\n放棄了？答案是 {secret}！")
            return attempts, False, name

        # 驗證輸入
        try:
            guess = int(guess_input)
        except ValueError:
            print("請輸入有效的數字！")
            continue

        if guess < min_num or guess > max_num:
            print(f"請輸入 {min_num} 到 {max_num} 之間的數字！")
            continue

        attempts += 1
        guesses.append(guess)

        # 判斷結果
        if guess == secret:
            print(f"""
🎉🎉🎉 恭喜！你猜對了！🎉🎉🎉

答案就是 {secret}！
你用了 {attempts} 次猜中！
""")
            # 評價
            if attempts <= 3:
                print("評價: 天才！🧠")
            elif attempts <= 5:
                print("評價: 優秀！⭐")
            elif attempts <= 8:
                print("評價: 不錯！👍")
            else:
                print("評價: 繼續加油！💪")

            return attempts, True, name

        elif guess < secret:
            diff = secret - guess
            if diff > max_num // 2:
                print("⬆️ 太小了！離答案還很遠...")
            elif diff > max_num // 4:
                print("⬆️ 太小了！但有點接近了")
            else:
                print("⬆️ 太小了！非常接近！🔥")
        else:
            diff = guess - secret
            if diff > max_num // 2:
                print("⬇️ 太大了！離答案還很遠...")
            elif diff > max_num // 4:
                print("⬇️ 太大了！但有點接近了")
            else:
                print("⬇️ 太大了！非常接近！🔥")

        # 顯示範圍提示
        smaller = [g for g in guesses if g < secret]
        larger = [g for g in guesses if g > secret]
        low_bound = max(smaller) if smaller else min_num
        high_bound = min(larger) if larger else max_num
        print(f"💡 目前範圍: {low_bound} ~ {high_bound}")

    # 使用完所有機會
    print(f"""
😢 很遺憾，機會用完了！

答案是 {secret}
你的猜測: {', '.join(map(str, guesses))}
""")
    return attempts, False, name


def main():
    print("""
╔══════════════════════════════════════════════════════╗
║              數字猜謎遊戲 v1.0                         ║
║           展示 Python 迴圈結構                         ║
╚══════════════════════════════════════════════════════╝
    """)

    stats = GameStats()

    # 使用 while True 實現主選單迴圈
    while True:
        print("""
【主選單】
  1. 開始遊戲 🎮
  2. 查看統計 📊
  3. 遊戲說明 📖
  0. 退出 👋
""")
        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n感謝遊玩！再見！👋")
            stats.show_stats()
            break

        elif choice == '1':
            difficulty = get_difficulty()
            attempts, won, diff_name = play_game(difficulty)
            stats.record_game(attempts, won, diff_name)
            input("\n按 Enter 繼續...")

        elif choice == '2':
            stats.show_stats()
            input("\n按 Enter 繼續...")

        elif choice == '3':
            print("""
📖 【遊戲說明】

這是一個經典的數字猜謎遊戲！

規則：
1. 電腦會隨機選擇一個範圍內的數字
2. 你需要猜測這個數字
3. 每次猜測後會告訴你猜大了還是猜小了
4. 在限定次數內猜中即為勝利

技巧：
- 使用二分法可以更快找到答案
- 注意提示中的「很遠」「接近」「非常接近」
- 查看範圍提示來縮小猜測範圍

迴圈結構的應用：
- while 迴圈：主選單和遊戲進行
- for 迴圈：統計計算和歷史顯示
- break：提前結束迴圈
- continue：跳過無效輸入
""")
            input("\n按 Enter 繼續...")

        else:
            print("無效的選項！")


if __name__ == "__main__":
    main()
