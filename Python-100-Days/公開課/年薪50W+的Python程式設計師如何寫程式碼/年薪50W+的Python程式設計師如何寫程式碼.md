## 年薪50W+的Python程式設計師如何寫程式碼

### 為什麼要用Python寫程式碼

#### 沒有對比就沒有傷害

> **很多網際網路和移動網際網路企業對開發效率的要求高於對執行效率的要求**。

##### 例子1：hello, world

C的版本：

```C
#include <stdio.h>

int main() {
    printf("hello, world\n");
    return 0;
}
```

Java的版本：

```Java
class Example01 {
    
    public static void main(String[] args) {
        System.out.println("hello, world");
    }
}
```

Python的版本：

```Python
print('hello, world')
```

#####  例子2：1-100求和

C的版本：

```C
#include <stdio.h>

int main() {
    int total = 0;
    for (int i = 1; i <= 100; ++i) {
        total += i;
    }
    printf("%d\n", total);
	return 0;
}
```

Python的版本：

```Java
print(sum(range(1, 101)))
```

##### 例子3：建立和初始化陣列（列表）

Java的版本：

```Java
import java.util.Arrays;

public class Example03 {

    public static void main(String[] args) {
        boolean[] values = new boolean[10];
        Arrays.fill(values, true);
        System.out.println(Arrays.toString(values));

        int[] numbers = new int[10];
        for (int i = 0; i < numbers.length; ++i) {
            numbers[i] = i + 1;
        }
        System.out.println(Arrays.toString(numbers));
    }
}
```

Python的版本：

```Python
values = [True] * 10
print(values)
numbers = [x for x in range(1, 11)]
print(numbers)
```

##### 例子4：雙色球隨機選號

Java的版本：

```Java
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

class Example03 {

    /**
     * 產生[min, max)範圍的隨機整數
     */
    public static int randomInt(int min, int max) {
        return (int) (Math.random() * (max - min) + min);
    }
    
    /**
     * 輸出一組雙色球號碼
     */
    public static void display(List<Integer> balls) {
        for (int i = 0; i < balls.size(); ++i) {
            System.out.printf("%02d ", balls.get(i));
            if (i == balls.size() - 2) {
                System.out.print("| ");
            }
        }
        System.out.println();
    }

    /**
     * 生成一組隨機號碼
     */
    public static List<Integer> generate() {
        List<Integer> redBalls = new ArrayList<>();
        for (int i = 1; i <= 33; ++i) {
            redBalls.add(i);
        }
        List<Integer> selectedBalls = new ArrayList<>();
        for (int i = 0; i < 6; ++i) {
            selectedBalls.add(redBalls.remove(randomInt(0, redBalls.size())));
        }
        Collections.sort(selectedBalls);
        selectedBalls.add(randomInt(1, 17));
        return selectedBalls;
    }
    
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            System.out.print("機選幾注: ");
            int num = sc.nextInt();
            for (int i = 0; i < num; ++i) {
                display(generate());
            }
        }
    }
}
```

Python的版本：

```Python
from random import randint, sample


def generate():
    """生成一組隨機號碼"""
    red_balls = [x for x in range(1, 34)]
    selected_balls = sample(red_balls, 6)
    selected_balls.sort()
    selected_balls.append(randint(1, 16))
    return selected_balls


def display(balls):
    """輸出一組雙色球號碼"""
    for index, ball in enumerate(balls):
        print(f'{ball:0>2d}', end=' ')
        if index == len(balls) - 2:
            print('|', end=' ')
    print()


num = int(input('機選幾注: '))
for _ in range(num):
    display(generate())
```

> **溫馨提示**：珍愛生命，遠離任何形式的賭博。

##### 例子5：實現一個簡單的HTTP伺服器。

Java的版本：

> **說明**：JDK 1.6以前，需要透過套接字程式設計來實現，具體又可以分為多執行緒和NIO兩種做法。JDK 1.6以後，可以使用`com.sun.net.httpserver`包提供的`HttpServer`類來實現。

```Java
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

class Example05 {

    public static void main(String[] arg) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new RequestHandler());
        server.start();
    }

    static class RequestHandler implements HttpHandler {
        
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "<h1>hello, world</h1>";
            exchange.sendResponseHeaders(200, 0);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response.getBytes());
            }
        }
    }
}
```

Python的版本：

```Python
from http.server import HTTPServer, SimpleHTTPRequestHandler


class RequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('<h1>hello, world</h1>'.encode())


server = HTTPServer(('', 8000), RequestHandler)
server.serve_forever()
```

或

```Python
python3 -m http.server 8000
```

#### 一行Python程式碼可以做什麼

> **很多時候，你的問題只需一行Python程式碼就能解決**。

```Python
# 一行程式碼實現求階乘函式
fac = lambda x: __import__('functools').reduce(int.__mul__, range(1, x + 1), 1)

# 一行程式碼實現求最大公約數函式
gcd = lambda x, y: y % x and gcd(y % x, x) or x

# 一行程式碼實現判斷素數的函式
is_prime = lambda x: x > 1 and not [f for f in range(2, int(x ** 0.5) + 1) if x % f == 0]

# 一行程式碼實現快速排序
quick_sort = lambda items: len(items) and quick_sort([x for x in items[1:] if x < items[0]]) + [items[0]] + quick_sort([x for x in items[1:] if x > items[0]]) or items

# 生成FizzBuzz列表
['Fizz'[x % 3 * 4:] + 'Buzz'[x % 5 * 4:] or x for x in range(1, 101)]
```

#### 設計模式從未如此簡單

> **Python是動態型別語言，大量的設計模式在Python中被簡化或弱化**。

思考：如何最佳化下面的程式碼。

```Python
def fib(num):
    if num in (1, 2):
        return 1
    return fib(num - 1) + fib(num - 2)
```

代理模式在Python中可以透過內建的或自定義的裝飾器來實現。

```Python
from functools import lru_cache


@lru_cache()
def fib(num):
    if num in (1, 2):
        return 1
    return fib(num - 1) + fib(num - 2)


for n in range(1, 121):
    print(f'{n}: {fib(n)}')
```

> **說明**：透過Python標準庫`functools`模組的`lru_cache`裝飾器為`fib`函式加上快取代理，快取函式執行的中間結果，最佳化程式碼的效能。

單例模式在Python中可以透過自定義的裝飾器或元類來實現。

```Python
from functools import wraps
from threading import RLock


def singleton(cls):
    instances = {}
    lock = RLock()

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
```

> **說明**：需要實現單例模式的類只需要新增上面的裝飾器即可。

原型模式在Python中可以透過元類來實現。

```Python
import copy


class PrototypeMeta(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.clone = lambda self, is_deep=True: \
            copy.deepcopy(self) if is_deep else copy.copy(self)
```

> **說明**：透過元類給指定了`metaclass=PrototypeMeta`的類新增一個`clone`方法實現物件克隆，利用Python標準庫`copy`模組的`copy`和`deepcopy`分別實現淺複製和深複製。

#### 資料採集和資料分析從未如此簡單

> **網路資料採集是Python最擅長的領域之一。**

例子：獲取豆瓣電影“Top250”。

```Python
import random
import time

import requests
from bs4 import BeautifulSoup

for page in range(10):
    resp = requests.get(
        url=f'https://movie.douban.com/top250?start={25 * page}',
        headers={'User-Agent': 'BaiduSpider'}
    )
    soup = BeautifulSoup(resp.text, "lxml")
    for elem in soup.select('a > span.title:nth-child(1)'):
        print(elem.text)
    time.sleep(random.random() * 5)
```

> **利用NumPy、Pandas、Matplotlib可以輕鬆實現資料分析和視覺化**。

![](res/use-pandas-in-jupyter-notebook.png)

### 寫出Python程式碼的正確姿勢

> **用Python寫程式碼就要寫出Pythonic的程式碼**。

#### 姿勢1：選擇結構的正確姿勢

跨界開發者的程式碼：

```Python
name = 'jackfrued'
fruits = ['apple', 'orange', 'grape']
owners = {'name': 'Kevin', 'age': 40, 'gender': True}
if name != '' and len(fruits) > 0 and len(owners.keys()) > 0:
    print('Jackfrued love fruits.')
```

Pythonic的程式碼：

```Python
name = 'jackfrued'
fruits = ['apple', 'orange', 'grape']
owners = {'name': 'Kevin', 'age': 40, 'gender': True}
if name and fruits and owners:
    print('Jackfrued love fruits.')
```

#### 姿勢2：交換兩個變數的正確姿勢

跨界開發者的程式碼：

```Python
temp = a
a = b
b = temp
```

或

```Python
a = a ^ b
b = a ^ b
a = a ^ b
```

Pythonic的程式碼：

```Python
a, b = b, a
```


#### 姿勢3：用序列組裝字串的正確姿勢

跨界開發者的程式碼：

```Python
chars = ['j', 'a', 'c', 'k', 'f', 'r', 'u', 'e', 'd']
name = ''
for char in chars:
    name += char
```

Pythonic的程式碼：

```Python
chars = ['j', 'a', 'c', 'k', 'f', 'r', 'u', 'e', 'd']
name = ''.join(chars)
```


#### 姿勢4：遍歷列表的正確姿勢

跨界開發者的程式碼：

```Python
fruits = ['orange', 'grape', 'pitaya', 'blueberry']
index = 0
for fruit in fruits:
    print(index, ':', fruit)
    index += 1
```

Pythonic的程式碼：

```Python
fruits = ['orange', 'grape', 'pitaya', 'blueberry']
for index, fruit in enumerate(fruits):
    print(index, ':', fruit)
```


#### 姿勢5：建立列表的正確姿勢

跨界開發者的程式碼：

```Python
data = [7, 20, 3, 15, 11]
result = []
for i in data:
    if i > 10:
        result.append(i * 3)
```

Pythonic的程式碼：

```Python
data = [7, 20, 3, 15, 11]
result = [num * 3 for num in data if num > 10]
```


#### 姿勢6：確保程式碼健壯性的正確姿勢

跨界開發者的程式碼：

```Python
data = {'x': '5'}
if 'x' in data and isinstance(data['x'], (str, int, float)) \
        and data['x'].isdigit():
    value = int(data['x'])
    print(value)
else:
    value = None
```

Pythonic的程式碼：

```Python
data = {'x': '5'}
try:
    value = int(data['x'])
    print(value)
except (KeyError, TypeError, ValueError):
    value = None
```


### 使用Lint工具檢查你的程式碼規範

閱讀下面的程式碼，看看你能看出哪些地方是有毛病的或者說不符合Python的程式設計規範的。

```Python
from enum import *

@unique
class Suite (Enum):
    SPADE, HEART, CLUB, DIAMOND = range(4)

class Card(object):
    def __init__(self,suite,face ):
        self.suite = suite
        self.face = face


    def __repr__(self):
        suites='♠♥♣♦'
        faces=['','A','2','3','4','5','6','7','8','9','10','J','Q','K']
        return f'{suites[self.suite.value]}{faces[self.face]}'

import random

class Poker(object):
    def __init__(self):
        self.cards =[Card(suite, face) for suite in Suite
            for face in range(1, 14)]
        self.current=0
    def shuffle (self):
        self.current=0
        random.shuffle(self.cards)
    def deal (self):
        card = self.cards[self.current]
        self.current+=1
        return card
    def has_next (self):
        if self.current<len(self.cards): return True
        return False

p = Poker()
p.shuffle()
print(p.cards)
```

#### PyLint的安裝和使用

Pylint是Python程式碼分析工具，它分析Python程式碼中的錯誤，查詢不符合程式碼風格標準（預設使用的程式碼風格是 PEP 8）和有潛在問題的程式碼。

```Bash
pip install pylint
pylint [options] module_or_package
```

Pylint輸出格式如下所示。

> 模組名:行號:列號:    訊息型別    訊息

訊息型別有以下幾種：

1. C - 慣例：違反了Python程式設計慣例（PEP 8）的程式碼。
2. R - 重構：寫得比較糟糕需要重構的程式碼。
3. W - 警告：程式碼中存在的不影響程式碼執行的問題。
4. E - 錯誤：程式碼中存在的影響程式碼執行的錯誤。
5. F - 致命錯誤：導致Pylint無法繼續執行的錯誤。

Pylint命令的常用引數：

1. `--disable=<msg ids>`或`-d <msg ids>`：禁用指定型別的訊息。
2. `--errors-only`或`-E`：只顯示錯誤。
3. `--rcfile=<file>`：指定配置檔案。
4. `--list-msgs`：列出Pylint的訊息清單。
5. `--generate-rcfile`：生成配置檔案的樣例。
6. `--reports=<y_or_n>`或`-r <y_or_n>`：是否生成檢查報告。

### 使用Profile工具剖析你的程式碼效能

#### cProfile模組

`example01.py`

```Python
import cProfile


def is_prime(num):
    for factor in range(2, int(num ** 0.5) + 1):
        if num % factor == 0:
            return False
    return True


class PrimeIter:

    def __init__(self, total):
        self.counter = 0
        self.current = 1
        self.total = total

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.total:
            self.current += 1
            while not is_prime(self.current):
                self.current += 1
            self.counter += 1
            return self.current
        raise StopIteration()

        
cProfile.run('list(PrimeIter(10000))')
```

執行結果：

```
   114734 function calls in 0.573 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.006    0.006    0.573    0.573 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 example.py:14(__init__)
        1    0.000    0.000    0.000    0.000 example.py:19(__iter__)
    10001    0.086    0.000    0.567    0.000 example.py:22(__next__)
   104728    0.481    0.000    0.481    0.000 example.py:5(is_prime)
        1    0.000    0.000    0.573    0.573 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

####line_profiler

給需要剖析時間效能的函式加上一個`profile`裝飾器，這個函式每行程式碼的執行次數和時間都會被剖析。

`example02.py`

```Python
@profile
def is_prime(num):
    for factor in range(2, int(num ** 0.5) + 1):
        if num % factor == 0:
            return False
    return True


class PrimeIter:

    def __init__(self, total):
        self.counter = 0
        self.current = 1
        self.total = total

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.total:
            self.current += 1
            while not is_prime(self.current):
                self.current += 1
            self.counter += 1
            return self.current
        raise StopIteration()


list(PrimeIter(1000))
```

安裝和使用`line_profiler`三方庫。

```Bash
pip install line_profiler
kernprof -lv example.py

Wrote profile results to example02.py.lprof
Timer unit: 1e-06 s

Total time: 0.089513 s
File: example02.py
Function: is_prime at line 1

 #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
 1                                           @profile
 2                                           def is_prime(num):
 3     86624      43305.0      0.5     48.4      for factor in range(2, int(num ** 0.5) + 1):
 4     85624      42814.0      0.5     47.8          if num % factor == 0:
 5      6918       3008.0      0.4      3.4              return False
 6      1000        386.0      0.4      0.4      return True
```

####memory_profiler 

給需要剖析記憶體效能的函式加上一個`profile`裝飾器，這個函式每行程式碼的記憶體使用情況都會被剖析。

`example03.py`

```Python
@profile
def eat_memory():
    items = []
    for _ in range(1000000):
        items.append(object())
    return items


eat_memory()
```

安裝和使用`memory_profiler`三方庫。

```Python
pip install memory_profiler
python3 -m memory_profiler example.py

Filename: example03.py

Line #    Mem usage    Increment   Line Contents
================================================
     1   38.672 MiB   38.672 MiB   @profile
     2                             def eat_memory():
     3   38.672 MiB    0.000 MiB       items = []
     4   68.727 MiB    0.000 MiB       for _ in range(1000000):
     5   68.727 MiB    1.797 MiB           items.append(object())
     6   68.727 MiB    0.000 MiB       return items
```

### 如何構建綜合職業素養

#### 學習總結

1. 瞭解全域性
2. 確定範圍
3. 定義目標
4. 尋找資源
5. 建立學習計劃
6. 篩選資源
7. 開始學習，淺嘗輒止（YAGNI）
8. 動手操作，邊學邊玩
9. 全面掌握，學以致用
10. 樂為人師，融會貫通

#### 時間管理

1. 提升專注力

2. 充分利用碎片時間

3. 使用番茄工作法

4. 時間是怎麼浪費掉的

5. 任何行動都比不採取行動好

   ![](res/action.png)


#### 好書推薦

1. 職業規劃：《軟技能 - 程式碼之外的生存指南》
2. 吳軍系列：《浪潮之巔》、《矽谷之謎》、《數學之美》、……
3. 時間管理：《成為一個更高效的人》、《番茄工作法圖解》