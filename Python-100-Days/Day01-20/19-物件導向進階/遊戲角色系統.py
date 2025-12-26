"""
遊戲角色系統 - Game Character System
=====================================
進階應用：展示 Python 物件導向進階概念

功能：
1. 繼承 (Inheritance)
2. 多型 (Polymorphism)
3. 抽象類別 (Abstract Class)
4. 方法覆寫 (Override)
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import random


# ========================================
# 1. 抽象基礎類別
# ========================================

class Character(ABC):
    """
    角色抽象基礎類別

    所有遊戲角色都繼承自此類別
    """

    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.max_hp = 100 + (level * 20)
        self.hp = self.max_hp
        self.max_mp = 50 + (level * 10)
        self.mp = self.max_mp
        self.exp = 0
        self.exp_to_level = level * 100
        self.is_alive = True
        self.buffs = []
        self.debuffs = []

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.name} (Lv.{self.level})"

    @abstractmethod
    def attack(self, target: 'Character') -> dict:
        """攻擊（子類必須實作）"""
        pass

    @abstractmethod
    def special_skill(self, target: 'Character') -> dict:
        """特殊技能（子類必須實作）"""
        pass

    @abstractmethod
    def get_role_description(self) -> str:
        """角色描述（子類必須實作）"""
        pass

    def take_damage(self, damage: int) -> int:
        """受到傷害"""
        actual_damage = max(0, damage - self.get_defense())
        self.hp = max(0, self.hp - actual_damage)

        if self.hp <= 0:
            self.is_alive = False

        return actual_damage

    def heal(self, amount: int) -> int:
        """治療"""
        if not self.is_alive:
            return 0

        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def use_mp(self, cost: int) -> bool:
        """消耗 MP"""
        if self.mp >= cost:
            self.mp -= cost
            return True
        return False

    def restore_mp(self, amount: int) -> int:
        """恢復 MP"""
        old_mp = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.mp - old_mp

    def gain_exp(self, exp: int):
        """獲得經驗值"""
        self.exp += exp
        while self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        """升級"""
        self.exp -= self.exp_to_level
        self.level += 1
        self.exp_to_level = self.level * 100

        # 提升屬性
        self.max_hp += 20
        self.max_mp += 10
        self.hp = self.max_hp
        self.mp = self.max_mp

    def get_defense(self) -> int:
        """取得防禦力（可覆寫）"""
        return self.level * 2

    def get_attack_power(self) -> int:
        """取得攻擊力（可覆寫）"""
        return 10 + self.level * 5

    def get_status(self) -> dict:
        """取得狀態"""
        return {
            'name': self.name,
            'class': self.__class__.__name__,
            'level': self.level,
            'hp': f"{self.hp}/{self.max_hp}",
            'mp': f"{self.mp}/{self.max_mp}",
            'exp': f"{self.exp}/{self.exp_to_level}",
            'is_alive': self.is_alive,
        }

    def display_status(self):
        """顯示狀態條"""
        hp_bar = self._make_bar(self.hp, self.max_hp, 20, '❤️')
        mp_bar = self._make_bar(self.mp, self.max_mp, 20, '💙')
        exp_bar = self._make_bar(self.exp, self.exp_to_level, 20, '⭐')

        print(f"\n{'='*40}")
        print(f"  {self}")
        print(f"  HP: {hp_bar} {self.hp}/{self.max_hp}")
        print(f"  MP: {mp_bar} {self.mp}/{self.max_mp}")
        print(f"  EXP: {exp_bar} {self.exp}/{self.exp_to_level}")
        print(f"{'='*40}")

    def _make_bar(self, current: int, maximum: int, length: int, char: str) -> str:
        """製作狀態條"""
        filled = int(current / maximum * length) if maximum > 0 else 0
        return '█' * filled + '░' * (length - filled)


# ========================================
# 2. 具體角色類別（繼承）
# ========================================

class Warrior(Character):
    """戰士 - 高攻擊、高防禦"""

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_hp += 50  # 額外生命值
        self.hp = self.max_hp
        self.rage = 0  # 怒氣值

    def get_role_description(self) -> str:
        return "⚔️ 戰士：近戰專家，擁有強大的攻擊力和防禦力"

    def get_defense(self) -> int:
        return self.level * 4  # 雙倍防禦

    def get_attack_power(self) -> int:
        return 15 + self.level * 7  # 較高攻擊

    def attack(self, target: 'Character') -> dict:
        """普通攻擊"""
        damage = self.get_attack_power()
        actual = target.take_damage(damage)
        self.rage = min(100, self.rage + 10)

        return {
            'action': '揮劍攻擊',
            'damage': actual,
            'message': f"{self.name} 對 {target.name} 造成 {actual} 點傷害！"
        }

    def special_skill(self, target: 'Character') -> dict:
        """旋風斬（消耗怒氣）"""
        if self.rage < 50:
            return {'success': False, 'message': '怒氣不足！(需要 50)'}

        self.rage -= 50
        damage = self.get_attack_power() * 2
        actual = target.take_damage(damage)

        return {
            'success': True,
            'action': '🌀 旋風斬',
            'damage': actual,
            'message': f"{self.name} 使出旋風斬，對 {target.name} 造成 {actual} 點傷害！"
        }


class Mage(Character):
    """法師 - 高魔法攻擊"""

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_mp += 50  # 額外魔力
        self.mp = self.max_mp

    def get_role_description(self) -> str:
        return "🔮 法師：魔法專家，擁有強大的範圍魔法攻擊"

    def get_defense(self) -> int:
        return self.level  # 較低防禦

    def get_attack_power(self) -> int:
        return 8 + self.level * 4  # 普攻較弱

    def get_magic_power(self) -> int:
        return 20 + self.level * 10

    def attack(self, target: 'Character') -> dict:
        """魔法彈（消耗少量 MP）"""
        mp_cost = 5
        if not self.use_mp(mp_cost):
            # MP 不足時使用杖擊
            damage = self.get_attack_power() // 2
            actual = target.take_damage(damage)
            return {
                'action': '杖擊',
                'damage': actual,
                'message': f"{self.name} 用法杖敲擊 {target.name}，造成 {actual} 點傷害！"
            }

        damage = self.get_magic_power()
        actual = target.take_damage(damage)

        return {
            'action': '✨ 魔法彈',
            'damage': actual,
            'message': f"{self.name} 發射魔法彈，對 {target.name} 造成 {actual} 點傷害！"
        }

    def special_skill(self, target: 'Character') -> dict:
        """火球術"""
        mp_cost = 30
        if not self.use_mp(mp_cost):
            return {'success': False, 'message': f'MP 不足！(需要 {mp_cost})'}

        damage = self.get_magic_power() * 3
        actual = target.take_damage(damage)

        return {
            'success': True,
            'action': '🔥 火球術',
            'damage': actual,
            'message': f"{self.name} 施放火球術，對 {target.name} 造成 {actual} 點傷害！"
        }


class Healer(Character):
    """治療師 - 支援型"""

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.max_mp += 30
        self.mp = self.max_mp

    def get_role_description(self) -> str:
        return "💚 治療師：支援專家，可以治療隊友"

    def get_attack_power(self) -> int:
        return 5 + self.level * 3  # 攻擊最弱

    def get_heal_power(self) -> int:
        return 30 + self.level * 15

    def attack(self, target: 'Character') -> dict:
        """神聖打擊"""
        damage = self.get_attack_power()
        actual = target.take_damage(damage)

        return {
            'action': '神聖打擊',
            'damage': actual,
            'message': f"{self.name} 對 {target.name} 造成 {actual} 點傷害！"
        }

    def special_skill(self, target: 'Character') -> dict:
        """治療術（可以對友軍使用）"""
        mp_cost = 20
        if not self.use_mp(mp_cost):
            return {'success': False, 'message': f'MP 不足！(需要 {mp_cost})'}

        heal_amount = self.get_heal_power()
        actual_heal = target.heal(heal_amount)

        return {
            'success': True,
            'action': '💖 治療術',
            'heal': actual_heal,
            'message': f"{self.name} 對 {target.name} 施放治療術，恢復 {actual_heal} HP！"
        }


class Archer(Character):
    """弓箭手 - 高爆擊"""

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.crit_rate = 0.3  # 30% 爆擊率

    def get_role_description(self) -> str:
        return "🏹 弓箭手：遠程專家，擁有高爆擊率"

    def get_attack_power(self) -> int:
        return 12 + self.level * 6

    def attack(self, target: 'Character') -> dict:
        """射擊"""
        is_crit = random.random() < self.crit_rate
        damage = self.get_attack_power()

        if is_crit:
            damage = int(damage * 2)
            action = '💥 爆擊射擊'
        else:
            action = '射擊'

        actual = target.take_damage(damage)

        return {
            'action': action,
            'damage': actual,
            'is_crit': is_crit,
            'message': f"{self.name} {'爆擊！' if is_crit else ''}對 {target.name} 造成 {actual} 點傷害！"
        }

    def special_skill(self, target: 'Character') -> dict:
        """多重箭矢"""
        mp_cost = 25
        if not self.use_mp(mp_cost):
            return {'success': False, 'message': f'MP 不足！(需要 {mp_cost})'}

        total_damage = 0
        hits = random.randint(3, 5)

        for _ in range(hits):
            damage = self.get_attack_power() // 2
            actual = target.take_damage(damage)
            total_damage += actual

        return {
            'success': True,
            'action': f'🏹 多重箭矢 x{hits}',
            'damage': total_damage,
            'message': f"{self.name} 發射 {hits} 支箭矢，共造成 {total_damage} 點傷害！"
        }


# ========================================
# 3. 怪物類別
# ========================================

class Monster(Character):
    """怪物基礎類別"""

    def __init__(self, name: str, level: int = 1):
        super().__init__(name, level)
        self.exp_reward = level * 20

    def get_role_description(self) -> str:
        return "👹 怪物"

    def attack(self, target: 'Character') -> dict:
        damage = self.get_attack_power()
        actual = target.take_damage(damage)

        return {
            'action': '攻擊',
            'damage': actual,
            'message': f"{self.name} 對 {target.name} 造成 {actual} 點傷害！"
        }

    def special_skill(self, target: 'Character') -> dict:
        return self.attack(target)


class Slime(Monster):
    """史萊姆"""

    def get_role_description(self) -> str:
        return "🟢 史萊姆：弱小的史萊姆"

    def get_attack_power(self) -> int:
        return 5 + self.level * 2


class Goblin(Monster):
    """哥布林"""

    def get_role_description(self) -> str:
        return "👺 哥布林：狡猾的哥布林"


class Dragon(Monster):
    """龍"""

    def __init__(self, name: str, level: int = 10):
        super().__init__(name, level)
        self.max_hp *= 3
        self.hp = self.max_hp
        self.exp_reward = level * 100

    def get_role_description(self) -> str:
        return "🐉 龍：強大的巨龍"

    def get_attack_power(self) -> int:
        return 30 + self.level * 10

    def special_skill(self, target: 'Character') -> dict:
        """龍息"""
        damage = self.get_attack_power() * 2
        actual = target.take_damage(damage)

        return {
            'success': True,
            'action': '🔥 龍息',
            'damage': actual,
            'message': f"{self.name} 噴出龍息，對 {target.name} 造成 {actual} 點傷害！"
        }


# ========================================
# 4. 戰鬥系統
# ========================================

class Battle:
    """戰鬥系統"""

    def __init__(self, player: Character, enemy: Monster):
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.log = []

    def player_turn(self, action: str) -> dict:
        """玩家回合"""
        if action == '1':
            result = self.player.attack(self.enemy)
        elif action == '2':
            result = self.player.special_skill(self.enemy)
            if not result.get('success', True):
                return result
        else:
            return {'message': '無效的行動'}

        self.log.append(f"[回合 {self.turn}] {result['message']}")
        return result

    def enemy_turn(self) -> dict:
        """敵人回合"""
        if random.random() < 0.3:
            result = self.enemy.special_skill(self.player)
        else:
            result = self.enemy.attack(self.player)

        self.log.append(f"[回合 {self.turn}] {result['message']}")
        return result

    def is_battle_over(self) -> tuple:
        """檢查戰鬥是否結束"""
        if not self.enemy.is_alive:
            return True, 'win'
        if not self.player.is_alive:
            return True, 'lose'
        return False, None


# ========================================
# 主程式
# ========================================

def main():
    print("""
╔══════════════════════════════════════════════════════╗
║             遊戲角色系統 v1.0                          ║
║           展示 Python 物件導向進階                     ║
╚══════════════════════════════════════════════════════╝
    """)

    player = None

    while True:
        status_text = f"角色: {player}" if player else "尚未創建角色"
        print(f"""
🎮 {status_text}

【選單】
  1. 創建角色        2. 查看狀態
  3. 戰鬥            4. 角色說明
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            print("\n⚔️ 創建角色")
            print("=" * 40)
            print("  1. 戰士 (高攻高防)")
            print("  2. 法師 (魔法攻擊)")
            print("  3. 治療師 (支援)")
            print("  4. 弓箭手 (高爆擊)")

            class_choice = input("\n選擇職業: ").strip()
            name = input("角色名稱: ").strip() or "冒險者"

            classes = {
                '1': Warrior,
                '2': Mage,
                '3': Healer,
                '4': Archer,
            }

            if class_choice in classes:
                player = classes[class_choice](name)
                print(f"\n✅ 創建成功！")
                print(f"   {player.get_role_description()}")
            else:
                print("❌ 無效的選擇！")

        elif choice == '2':
            if not player:
                print("❌ 請先創建角色！")
                continue

            player.display_status()
            print(f"  攻擊力: {player.get_attack_power()}")
            print(f"  防禦力: {player.get_defense()}")

            if isinstance(player, Warrior):
                print(f"  怒氣值: {player.rage}/100")
            elif isinstance(player, Mage):
                print(f"  魔力: {player.get_magic_power()}")
            elif isinstance(player, Healer):
                print(f"  治療量: {player.get_heal_power()}")
            elif isinstance(player, Archer):
                print(f"  爆擊率: {player.crit_rate * 100:.0f}%")

        elif choice == '3':
            if not player:
                print("❌ 請先創建角色！")
                continue

            print("\n⚔️ 選擇敵人")
            print("=" * 40)
            print("  1. 史萊姆 (簡單)")
            print("  2. 哥布林 (普通)")
            print("  3. 巨龍 (困難)")

            enemy_choice = input("\n選擇: ").strip()

            enemies = {
                '1': lambda: Slime("史萊姆", player.level),
                '2': lambda: Goblin("哥布林", player.level + 1),
                '3': lambda: Dragon("火焰巨龍", player.level + 5),
            }

            if enemy_choice not in enemies:
                print("❌ 無效的選擇！")
                continue

            enemy = enemies[enemy_choice]()
            battle = Battle(player, enemy)

            print(f"\n⚔️ 戰鬥開始！{player.name} vs {enemy.name}")
            print("=" * 50)

            while True:
                print(f"\n--- 回合 {battle.turn} ---")
                print(f"{player.name}: HP {player.hp}/{player.max_hp} | MP {player.mp}/{player.max_mp}")
                print(f"{enemy.name}: HP {enemy.hp}/{enemy.max_hp}")

                print("\n行動: 1.攻擊  2.技能  3.逃跑")
                action = input("選擇: ").strip()

                if action == '3':
                    print("你逃跑了！")
                    break

                # 玩家行動
                result = battle.player_turn(action)
                print(f"\n{result['message']}")

                over, outcome = battle.is_battle_over()
                if over:
                    break

                # 敵人行動
                result = battle.enemy_turn()
                print(f"{result['message']}")

                over, outcome = battle.is_battle_over()
                if over:
                    break

                battle.turn += 1
                input("\n按 Enter 繼續...")

            if outcome == 'win':
                exp = enemy.exp_reward
                print(f"\n🎉 勝利！獲得 {exp} 經驗值！")
                old_level = player.level
                player.gain_exp(exp)
                if player.level > old_level:
                    print(f"🎊 升級！達到 Lv.{player.level}！")
                player.hp = player.max_hp
                player.mp = player.max_mp
            elif outcome == 'lose':
                print("\n💀 戰敗...")
                player.hp = player.max_hp // 2
                player.is_alive = True

        elif choice == '4':
            print("\n📖 角色說明")
            print("=" * 50)

            classes = [Warrior, Mage, Healer, Archer]
            for cls in classes:
                temp = cls("範例", 1)
                print(f"\n{temp.get_role_description()}")
                print(f"  基礎攻擊: {temp.get_attack_power()}")
                print(f"  基礎防禦: {temp.get_defense()}")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
