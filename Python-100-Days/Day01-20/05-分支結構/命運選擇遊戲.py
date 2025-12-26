"""
命運選擇遊戲 - Destiny Choice Game
==================================
進階應用：展示 Python 分支結構的互動式應用

功能：
1. 文字冒險遊戲
2. 多重分支選擇
3. 狀態追蹤
4. 多結局系統
"""

import random


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.gold = 50
        self.items = []
        self.karma = 0  # 善惡值

    def status(self):
        karma_text = "善良 😇" if self.karma > 5 else "邪惡 😈" if self.karma < -5 else "中立 😐"
        return f"""
┌─────────────────────────────┐
│ 👤 {self.name:^25} │
├─────────────────────────────┤
│ ❤️  生命: {self.health:>3}/100             │
│ 💰 金幣: {self.gold:>3}                  │
│ 🎒 物品: {len(self.items):>2} 個                │
│ ⚖️  性格: {karma_text:^10}         │
└─────────────────────────────┘
"""


def intro(player):
    print(f"""
╔══════════════════════════════════════════════════════╗
║              命運選擇遊戲 v1.0                         ║
║         展示 Python 分支結構的力量                      ║
╚══════════════════════════════════════════════════════╝

{player.name}，你在一個神秘的森林中醒來...
四周一片寂靜，遠處傳來若隱若現的聲音。
""")


def scene_forest(player):
    print("""
🌲 【神秘森林】

你站在森林的分岔路口，看到三條道路：

  1. 向左走 - 通往一座古老的城堡 🏰
  2. 向右走 - 通往一個熱鬧的村莊 🏘️
  3. 直走   - 深入黑暗的森林深處 🌑
  4. 查看狀態
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '4':
            print(player.status())
            continue
        elif choice == '1':
            return scene_castle(player)
        elif choice == '2':
            return scene_village(player)
        elif choice == '3':
            return scene_deep_forest(player)
        else:
            print("請輸入有效的選項！")


def scene_castle(player):
    print("""
🏰 【古老城堡】

你來到一座陰森的城堡前。城門半開著，裡面傳來微弱的光芒。
一個守衛攔住了你。

守衛：「來者何人？想進入城堡必須證明你的誠意！」

  1. 賄賂守衛 (需要 30 金幣) 💰
  2. 與守衛戰鬥 ⚔️
  3. 說服守衛讓你進入 🗣️
  4. 返回森林 🔙
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '1':
            if player.gold >= 30:
                player.gold -= 30
                player.karma -= 2
                print("\n守衛收下金幣，讓你進入了城堡。")
                print("(-30 金幣, 善惡值 -2)")
                return scene_castle_inside(player)
            else:
                print("\n你的金幣不夠！")

        elif choice == '2':
            damage = random.randint(10, 30)
            player.health -= damage
            player.karma -= 3
            print(f"\n你與守衛激戰！受到 {damage} 點傷害。")
            print(f"(生命值 -{damage}, 善惡值 -3)")

            if player.health <= 0:
                return "defeat"

            print("你最終擊敗了守衛，但良心受到譴責...")
            return scene_castle_inside(player)

        elif choice == '3':
            # 善惡值影響結果
            if player.karma >= 0:
                print("\n守衛看出你眼中的善意，決定讓你通過。")
                print("(善惡值 +1)")
                player.karma += 1
                return scene_castle_inside(player)
            else:
                print("\n守衛感受到你的惡意，拒絕讓你通過！")
                print("你只能選擇其他方式。")

        elif choice == '4':
            return scene_forest(player)
        else:
            print("請輸入有效的選項！")


def scene_castle_inside(player):
    print("""
🏰 【城堡內部】

城堡內金碧輝煌。你發現一個寶箱和一扇神秘的門。

  1. 打開寶箱 📦
  2. 進入神秘之門 🚪
  3. 離開城堡 🔙
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '1':
            gold_found = random.randint(20, 50)
            player.gold += gold_found
            player.items.append("寶石")
            print(f"\n🎉 你發現了 {gold_found} 金幣和一顆寶石！")
            return scene_castle_inside(player)

        elif choice == '2':
            if "神秘鑰匙" in player.items:
                print("\n你用神秘鑰匙打開了門...")
                return "good_ending"
            else:
                print("\n門被鎖住了，需要神秘鑰匙才能打開。")

        elif choice == '3':
            return scene_forest(player)
        else:
            print("請輸入有效的選項！")


def scene_village(player):
    print("""
🏘️ 【和平村莊】

這是一個溫馨的小村莊。村民們友善地向你打招呼。
你看到幾個地方可以去：

  1. 商店 - 購買物品 🛒
  2. 酒館 - 聽取情報 🍺
  3. 幫助村民 - 完成任務 ❤️
  4. 返回森林 🔙
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '1':
            return scene_shop(player)
        elif choice == '2':
            print("\n酒館老闆悄悄告訴你：")
            print("「聽說城堡裡有個神秘的門，需要特殊的鑰匙...」")
            print("「那把鑰匙似乎藏在森林深處的某個地方。」")
            input("\n按 Enter 繼續...")
            return scene_village(player)
        elif choice == '3':
            return scene_help_villager(player)
        elif choice == '4':
            return scene_forest(player)
        else:
            print("請輸入有效的選項！")


def scene_shop(player):
    print(f"""
🛒 【村莊商店】

店主：「歡迎光臨！」

你有 {player.gold} 金幣。

  1. 購買治療藥水 (20 金幣) 🧪 - 恢復 30 生命
  2. 購買護身符 (50 金幣) 🔮 - 防禦加成
  3. 離開商店 🔙
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '1':
            if player.gold >= 20:
                player.gold -= 20
                player.health = min(100, player.health + 30)
                player.items.append("治療藥水")
                print("\n你購買了治療藥水！生命值恢復 30 點。")
            else:
                print("\n金幣不夠！")
        elif choice == '2':
            if player.gold >= 50:
                player.gold -= 50
                player.items.append("護身符")
                print("\n你購買了護身符！")
            else:
                print("\n金幣不夠！")
        elif choice == '3':
            return scene_village(player)
        else:
            print("請輸入有效的選項！")


def scene_help_villager(player):
    print("""
❤️ 【幫助村民】

一位老奶奶向你求助：「好心人，能幫我找回走失的貓咪嗎？」

  1. 接受任務 ✅
  2. 拒絕並離開 ❌
""")

    choice = input("\n你的選擇是? ").strip()

    if choice == '1':
        print("\n你花了一些時間在村莊四處尋找...")
        if random.random() > 0.3:
            player.karma += 5
            player.gold += 25
            print("🎉 你找到了貓咪！老奶奶非常感謝你！")
            print("(+25 金幣, 善惡值 +5)")
        else:
            player.karma += 2
            print("雖然沒找到貓咪，但老奶奶感謝你的努力。")
            print("(善惡值 +2)")
    else:
        player.karma -= 2
        print("\n老奶奶失望地看著你離開。")
        print("(善惡值 -2)")

    input("\n按 Enter 繼續...")
    return scene_village(player)


def scene_deep_forest(player):
    print("""
🌑 【森林深處】

四周一片黑暗，你小心翼翼地前進。
突然，你發現地上有一個發光的物體！

  1. 撿起發光物體 ✨
  2. 忽略它繼續前進 ➡️
  3. 返回森林入口 🔙
""")

    while True:
        choice = input("\n你的選擇是? ").strip()

        if choice == '1':
            if "神秘鑰匙" not in player.items:
                player.items.append("神秘鑰匙")
                print("\n🔑 你獲得了【神秘鑰匙】！")
                print("這似乎是打開某扇門的關鍵...")
            else:
                player.gold += 10
                print("\n你發現了一些金幣！(+10 金幣)")
            input("\n按 Enter 繼續...")
            return scene_forest(player)

        elif choice == '2':
            # 隨機遭遇
            if random.random() > 0.5:
                damage = random.randint(5, 15)
                player.health -= damage
                print(f"\n你踩到了陷阱！受到 {damage} 點傷害。")
                if player.health <= 0:
                    return "defeat"
            else:
                player.gold += 20
                print("\n你發現了一個隱藏的寶藏！(+20 金幣)")
            input("\n按 Enter 繼續...")
            return scene_forest(player)

        elif choice == '3':
            return scene_forest(player)
        else:
            print("請輸入有效的選項！")


def show_ending(player, ending):
    print("\n" + "=" * 50)

    if ending == "good_ending":
        print("""
🎊 【好結局】

你用神秘鑰匙打開了神秘之門，
發現了傳說中的寶藏！

你帶著財富離開了這片土地，
成為了傳說中的英雄！

        🏆 恭喜通關！🏆
""")
    elif ending == "defeat":
        print("""
💀 【遊戲結束】

你的生命值歸零...
這片森林將成為你永遠的歸宿。

        請重新開始遊戲
""")

    print("=" * 50)
    print(player.status())


def main():
    print("歡迎來到命運選擇遊戲！")
    name = input("\n請輸入你的名字: ").strip() or "冒險者"

    player = Player(name)
    intro(player)

    result = scene_forest(player)

    while result not in ["good_ending", "defeat"]:
        result = result  # 場景會返回下一個場景或結局

        if isinstance(result, str) and result in ["good_ending", "defeat"]:
            break

    show_ending(player, result)


if __name__ == "__main__":
    main()
