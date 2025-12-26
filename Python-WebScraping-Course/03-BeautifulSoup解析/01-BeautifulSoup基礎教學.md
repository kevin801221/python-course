# BeautifulSoup 基礎教學

> Python 最受歡迎的 HTML 解析函式庫

## 什麼是 BeautifulSoup?

BeautifulSoup 是一個用於解析 HTML 和 XML 文件的 Python 函式庫。它能將複雜的 HTML 文件轉換成易於操作的樹狀結構，讓你可以輕鬆地擷取所需的資料。

### 名稱由來

「Beautiful Soup」這個名字來自《愛麗絲夢遊仙境》中的一首歌，暗示了這個函式庫能夠處理格式混亂的 HTML（又稱 "tag soup"）。

## 安裝 BeautifulSoup

```bash
# 使用 uv (推薦)
uv pip install beautifulsoup4 lxml

# 或使用 pip
pip install beautifulsoup4 lxml
```

## 基本使用

### 建立 BeautifulSoup 物件

```python
import requests
from bs4 import BeautifulSoup

# 取得網頁內容
url = "https://example.com"
response = requests.get(url)

# 建立 BeautifulSoup 物件
soup = BeautifulSoup(response.content, 'html.parser')
# 或使用 lxml 解析器 (更快)
# soup = BeautifulSoup(response.content, 'lxml')

print(soup.prettify())  # 美化輸出 HTML
```

## 常用選擇器方法

### find() - 找到第一個符合的元素

```python
from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <h1 id="title">網頁標題</h1>
        <div class="content">
            <p>第一段</p>
            <p>第二段</p>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

# 透過標籤名稱
title = soup.find('h1')
print(title.text)  # 網頁標題

# 透過 ID
title = soup.find(id='title')
print(title.text)  # 網頁標題

# 透過 class
content = soup.find('div', class_='content')
print(content)
```

### find_all() - 找到所有符合的元素

```python
# 找到所有 <p> 標籤
paragraphs = soup.find_all('p')
for p in paragraphs:
    print(p.text)

# 找到所有特定 class 的元素
items = soup.find_all('div', class_='item')

# 找到前 5 個元素
first_five = soup.find_all('p', limit=5)
```

### select() - 使用 CSS 選擇器

```python
# 透過 CSS 選擇器選取 (非常強大!)
soup.select('div.content')        # class="content" 的 div
soup.select('#title')             # id="title" 的元素
soup.select('div > p')            # div 的直接子元素 p
soup.select('div p')              # div 內所有的 p
soup.select('a[href]')            # 有 href 屬性的 a
soup.select('a[href^="https"]')   # href 以 https 開頭的 a
```

## 擷取資料

### 取得文字內容

```python
element = soup.find('h1')

# 取得文字
print(element.text)           # 包含所有子元素的文字
print(element.string)         # 只有直接文字內容
print(element.get_text())     # 同 .text
print(element.get_text(strip=True))  # 去除空白
```

### 取得屬性值

```python
link = soup.find('a')

# 取得 href 屬性
print(link['href'])
print(link.get('href'))  # 如果不存在會回傳 None

# 取得所有屬性
print(link.attrs)  # {'href': 'https://...', 'class': ['link']}
```

## 瀏覽 DOM 樹

### 存取父元素、子元素、兄弟元素

```python
element = soup.find('p')

# 父元素
parent = element.parent
print(parent.name)

# 所有祖先元素
for ancestor in element.parents:
    print(ancestor.name)

# 子元素
children = element.children  # 直接子元素 (generator)
descendants = element.descendants  # 所有後代元素

# 兄弟元素
next_sibling = element.next_sibling
prev_sibling = element.previous_sibling

# 下一個/上一個元素
next_element = element.next_element
prev_element = element.previous_element
```

## 使用正規表達式

```python
import re

# 找到所有 class 包含 "item" 的元素
items = soup.find_all(class_=re.compile('item'))

# 找到所有 href 以 https 開頭的連結
links = soup.find_all('a', href=re.compile('^https'))
```

## 使用函式過濾

```python
# 自訂過濾函式
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

results = soup.find_all(has_class_but_no_id)

# 使用 lambda 函式
python_jobs = soup.find_all(
    'h2',
    string=lambda text: text and 'python' in text.lower()
)
```

## 實戰範例：爬取工作列表

```python
import requests
from bs4 import BeautifulSoup

# 取得網頁
url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 找到所有工作卡片
job_cards = soup.find_all('div', class_='card-content')

jobs = []
for card in job_cards:
    job = {
        'title': card.find('h2', class_='title').text.strip(),
        'company': card.find('h3', class_='company').text.strip(),
        'location': card.find('p', class_='location').text.strip(),
    }

    # 取得申請連結
    links = card.find_all('a')
    if len(links) > 1:
        job['apply_url'] = links[1]['href']

    jobs.append(job)

# 輸出結果
for job in jobs[:5]:
    print(f"職位: {job['title']}")
    print(f"公司: {job['company']}")
    print(f"地點: {job['location']}")
    print(f"連結: {job.get('apply_url', 'N/A')}")
    print('-' * 50)
```

## 處理表格資料

```python
# 假設有一個 HTML 表格
table = soup.find('table')

# 取得所有列
rows = table.find_all('tr')

data = []
for row in rows:
    cols = row.find_all(['td', 'th'])
    row_data = [col.text.strip() for col in cols]
    data.append(row_data)

# 轉換為 DataFrame
import pandas as pd
df = pd.DataFrame(data[1:], columns=data[0])
print(df)
```

## 常見問題與解決方案

### 問題 1: 找不到元素 (返回 None)

```python
# 安全的取值方式
element = soup.find('div', class_='content')
if element:
    text = element.text
else:
    text = "找不到內容"

# 或使用 try-except
try:
    text = soup.find('div', class_='content').text
except AttributeError:
    text = "找不到內容"
```

### 問題 2: 動態內容無法擷取

BeautifulSoup 只能解析靜態 HTML，無法執行 JavaScript。如果內容是由 JavaScript 動態載入的，需要使用 Selenium 或 Playwright。

### 問題 3: 編碼問題

```python
# 使用 response.content 而非 response.text
soup = BeautifulSoup(response.content, 'html.parser')

# 或指定編碼
soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
```

## 解析器比較

| 解析器 | 速度 | 容錯性 | 安裝 |
|--------|------|--------|------|
| `html.parser` | 中等 | 好 | 內建 |
| `lxml` | 最快 | 非常好 | 需安裝 |
| `lxml-xml` | 快 | 非常好 | 需安裝 |
| `html5lib` | 慢 | 最好 | 需安裝 |

## 下一步

學會 BeautifulSoup 後，接下來學習如何使用 Selenium 處理動態網頁。

---

*參考資源：Real Python, ScrapingBee (2024-2025)*
