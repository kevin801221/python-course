#!/usr/bin/env python3
"""
從 19.面向对象编程进阶.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
class Student:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def study(self, course_name):
        print(f'{self.__name}正在學習{course_name}.')


stu = Student('王大錘', 20)
stu.study('Python程式設計')
print(stu.__name)  # AttributeError: 'Student' object has no attribute '__name'
# === 範例 2 ===
class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('王大錘', 20)
stu.sex = '男'  # 給學生物件動態新增sex屬性
# === 範例 3 ===
class Student:
    __slots__ = ('name', 'age')

    def __init__(self, name, age):
        self.name = name
        self.age = age


stu = Student('王大錘', 20)
# AttributeError: 'Student' object has no attribute 'sex'
stu.sex = '男'
# === 範例 4 ===
class Triangle(object):
    """三角形"""

    def __init__(self, a, b, c):
        """初始化方法"""
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def is_valid(a, b, c):
        """判斷三條邊長能否構成三角形(靜態方法)"""
        return a + b > c and b + c > a and a + c > b

    # @classmethod
    # def is_valid(cls, a, b, c):
    #     """判斷三條邊長能否構成三角形(類方法)"""
    #     return a + b > c and b + c > a and a + c > b

    def perimeter(self):
        """計算周長"""
        return self.a + self.b + self.c

    def area(self):
        """計算面積"""
        p = self.perimeter() / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5
# === 範例 5 ===
class Triangle(object):
    """三角形"""

    def __init__(self, a, b, c):
        """初始化方法"""
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def is_valid(a, b, c):
        """判斷三條邊長能否構成三角形(靜態方法)"""
        return a + b > c and b + c > a and a + c > b

    @property
    def perimeter(self):
        """計算周長"""
        return self.a + self.b + self.c

    @property
    def area(self):
        """計算面積"""
        p = self.perimeter / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5


t = Triangle(3, 4, 5)
print(f'周長: {t.perimeter}')
print(f'面積: {t.area}')
# === 範例 6 ===
class Person:
    """人"""

    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def eat(self):
        print(f'{self.name}正在吃飯.')
    
    def sleep(self):
        print(f'{self.name}正在睡覺.')


class Student(Person):
    """學生"""
    
    def __init__(self, name, age):
        super().__init__(name, age)
    
    def study(self, course_name):
        print(f'{self.name}正在學習{course_name}.')


class Teacher(Person):
    """老師"""

    def __init__(self, name, age, title):
        super().__init__(name, age)
        self.title = title
    
    def teach(self, course_name):
        print(f'{self.name}{self.title}正在講授{course_name}.')



stu1 = Student('白元芳', 21)
stu2 = Student('狄仁傑', 22)
tea1 = Teacher('武則天', 35, '副教授')
stu1.eat()
stu2.sleep()
tea1.eat()
stu1.study('Python程式設計')
tea1.teach('Python程式設計')
stu2.study('資料科學導論')
