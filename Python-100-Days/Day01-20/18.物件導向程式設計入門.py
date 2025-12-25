#!/usr/bin/env python3
"""
從 18.面向对象编程入门.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
class Student:

    def study(self, course_name):
        print(f'學生正在學習{course_name}.')

    def play(self):
        print(f'學生正在玩遊戲.')
# === 範例 2 ===
stu1 = Student()
stu2 = Student()
print(stu1)    # <__main__.Student object at 0x10ad5ac50>
print(stu2)    # <__main__.Student object at 0x10ad5acd0> 
print(hex(id(stu1)), hex(id(stu2)))    # 0x10ad5ac50 0x10ad5acd0
# === 範例 3 ===
# 透過“類.方法”呼叫方法
# 第一個引數是接收訊息的物件
# 第二個引數是學習的課程名稱
Student.study(stu1, 'Python程式設計')    # 學生正在學習Python程式設計.
# 透過“物件.方法”呼叫方法
# 點前面的物件就是接收訊息的物件
# 只需要傳入第二個引數課程名稱
stu1.study('Python程式設計')             # 學生正在學習Python程式設計.

Student.play(stu2)                      # 學生正在玩遊戲.
stu2.play()                             # 學生正在玩遊戲.
# === 範例 4 ===
class Student:
    """學生"""

    def __init__(self, name, age):
        """初始化方法"""
        self.name = name
        self.age = age

    def study(self, course_name):
        """學習"""
        print(f'{self.name}正在學習{course_name}.')

    def play(self):
        """玩耍"""
        print(f'{self.name}正在玩遊戲.')
# === 範例 5 ===
# 呼叫Student類的構造器建立物件並傳入初始化引數
stu1 = Student('Kevin', 44)
stu2 = Student('王大錘', 25)
stu1.study('Python程式設計')    # Kevin正在學習Python程式設計.
stu2.play()                    # 王大錘正在玩遊戲.
# === 範例 6 ===
import time


# 定義時鐘類
class Clock:
    """數字時鐘"""

    def __init__(self, hour=0, minute=0, second=0):
        """初始化方法
        :param hour: 時
        :param minute: 分
        :param second: 秒
        """
        self.hour = hour
        self.min = minute
        self.sec = second

    def run(self):
        """走字"""
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
            if self.min == 60:
                self.min = 0
                self.hour += 1
                if self.hour == 24:
                    self.hour = 0

    def show(self):
        """顯示時間"""
        return f'{self.hour:0>2d}:{self.min:0>2d}:{self.sec:0>2d}'


# 建立時鐘物件
clock = Clock(23, 59, 58)
while True:
    # 給時鐘物件發訊息讀取時間
    print(clock.show())
    # 休眠1秒鐘
    time.sleep(1)
    # 給時鐘物件發訊息使其走字
    clock.run()
# === 範例 7 ===
class Point:
    """平面上的點"""

    def __init__(self, x=0, y=0):
        """初始化方法
        :param x: 橫座標
        :param y: 縱座標
        """
        self.x, self.y = x, y

    def distance_to(self, other):
        """計算與另一個點的距離
        :param other: 另一個點
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5

    def __str__(self):
        return f'({self.x}, {self.y})'


p1 = Point(3, 5)
p2 = Point(6, 9)
print(p1)  # 呼叫物件的__str__魔法方法
print(p2)
print(p1.distance_to(p2))
