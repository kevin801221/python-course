#!/usr/bin/env python3
"""
從 20.面向对象编程应用.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from enum import Enum


class Suite(Enum):
    """花色(列舉)"""
    SPADE, HEART, CLUB, DIAMOND = range(4)
# === 範例 2 ===
for suite in Suite:
    print(f'{suite}: {suite.value}')
# === 範例 3 ===
class Card:
    """牌"""

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    def __repr__(self):
        suites = '♠♥♣♦'
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f'{suites[self.suite.value]}{faces[self.face]}'  # 返回牌的花色和點數
# === 範例 4 ===
card1 = Card(Suite.SPADE, 5)
card2 = Card(Suite.HEART, 13)
print(card1)  # ♠5 
print(card2)  # ♥K
# === 範例 5 ===
import random


class Poker:
    """撲克"""

    def __init__(self):
        self.cards = [Card(suite, face) 
                      for suite in Suite
                      for face in range(1, 14)]  # 52張牌構成的列表
        self.current = 0  # 記錄發牌位置的屬性

    def shuffle(self):
        """洗牌"""
        self.current = 0
        random.shuffle(self.cards)  # 透過random模組的shuffle函式實現隨機亂序

    def deal(self):
        """發牌"""
        card = self.cards[self.current]
        self.current += 1
        return card

    @property
    def has_next(self):
        """還有沒有牌可以發"""
        return self.current < len(self.cards)
# === 範例 6 ===
poker = Poker()
print(poker.cards)  # 洗牌前的牌
poker.shuffle()
print(poker.cards)  # 洗牌後的牌
# === 範例 7 ===
class Player:
    """玩家"""

    def __init__(self, name):
        self.name = name
        self.cards = []  # 玩家手上的牌

    def get_one(self, card):
        """摸牌"""
        self.cards.append(card)

    def arrange(self):
        """整理手上的牌"""
        self.cards.sort()
# === 範例 8 ===
poker = Poker()
poker.shuffle()
players = [Player('東邪'), Player('西毒'), Player('南帝'), Player('北丐')]
# 將牌輪流發到每個玩家手上每人13張牌
for _ in range(13):
    for player in players:
        player.get_one(poker.deal())
# 玩家整理手上的牌輸出名字和手牌
for player in players:
    player.arrange()
    print(f'{player.name}: ', end='')
    print(player.cards)
# === 範例 9 ===
class Card:
    """牌"""

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    def __repr__(self):
        suites = '♠♥♣♦'
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f'{suites[self.suite.value]}{faces[self.face]}'
    
    def __lt__(self, other):
        if self.suite == other.suite:
            return self.face < other.face   # 花色相同比較點數的大小
        return self.suite.value < other.suite.value   # 花色不同比較花色對應的值
# === 範例 10 ===
from abc import ABCMeta, abstractmethod


class Employee(metaclass=ABCMeta):
    """員工"""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_salary(self):
        """結算月薪"""
        pass
# === 範例 11 ===
class Manager(Employee):
    """部門經理"""

    def get_salary(self):
        return 15000.0


class Programmer(Employee):
    """程式設計師"""

    def __init__(self, name, working_hour=0):
        super().__init__(name)
        self.working_hour = working_hour

    def get_salary(self):
        return 200 * self.working_hour


class Salesman(Employee):
    """銷售員"""

    def __init__(self, name, sales=0):
        super().__init__(name)
        self.sales = sales

    def get_salary(self):
        return 1800 + self.sales * 0.05
# === 範例 12 ===
emps = [Manager('劉備'), Programmer('諸葛亮'), Manager('曹操'), Programmer('荀彧'), Salesman('張遼')]
for emp in emps:
    if isinstance(emp, Programmer):
        emp.working_hour = int(input(f'請輸入{emp.name}本月工作時間: '))
    elif isinstance(emp, Salesman):
        emp.sales = float(input(f'請輸入{emp.name}本月銷售額: '))
    print(f'{emp.name}本月工資為: ￥{emp.get_salary():.2f}元')
