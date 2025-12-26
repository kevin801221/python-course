# Requests 基礎教學

> Python 最受歡迎的 HTTP 請求函式庫

## 什麼是 Requests?

Requests 是 Python 中最流行的 HTTP 請求函式庫，下載量超過 1100 萬次。它大大簡化了發送 HTTP 請求的過程，讓程式碼更易讀、更易維護。

## 安裝 Requests

```bash
# 使用 uv (推薦)
uv pip install requests

# 或使用 pip
pip install requests
```

## 基本使用

### 發送 GET 請求

```python
import requests

# 發送 GET 請求
response = requests.get('https://www.example.com')

# 取得回應內容
print(response.text)  # HTML 文字內容
print(response.content)  # 原始位元組內容
print(response.status_code)  # HTTP 狀態碼 (200 表示成功)
```

### 發送 POST 請求

```python
import requests

# 發送表單資料
form_data = {'username': 'user', 'password': 'pass'}
response = requests.post('https://httpbin.org/post', data=form_data)

print(response.json())  # 解析 JSON 回應
```

### 發送 JSON 資料

```python
import requests

json_data = {'key': 'value', 'name': 'Python'}
response = requests.post('https://httpbin.org/post', json=json_data)

print(response.json())
```

## 設定請求標頭 (Headers)

```python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
}

response = requests.get('https://www.example.com', headers=headers)
print(response.text)
```

## 處理查詢參數

```python
import requests

# 方法一：直接在 URL 中加入參數
response = requests.get('https://api.example.com/search?q=python&page=1')

# 方法二：使用 params 參數 (推薦)
params = {
    'q': 'python',
    'page': 1,
    'sort': 'date'
}
response = requests.get('https://api.example.com/search', params=params)

print(response.url)  # 查看完整 URL
```

## 使用代理 (Proxy)

```python
import requests

proxies = {
    'http': 'http://user:pass@proxy.example.com:8080',
    'https': 'http://user:pass@proxy.example.com:8080',
}

response = requests.get('https://www.example.com', proxies=proxies)
```

## Session 管理

使用 Session 可以保持 cookies 和連線，適合需要登入的網站：

```python
import requests

# 建立 Session
session = requests.Session()

# 登入
login_data = {'username': 'user', 'password': 'pass'}
session.post('https://example.com/login', data=login_data)

# 後續請求會自動帶上 cookies
response = session.get('https://example.com/dashboard')
print(response.text)
```

## 下載檔案

### 下載圖片

```python
import requests

url = 'https://example.com/image.jpg'
response = requests.get(url)

with open('image.jpg', 'wb') as f:
    f.write(response.content)
```

### 下載大型檔案 (串流方式)

```python
import requests

url = 'https://example.com/large-file.zip'

with requests.get(url, stream=True) as response:
    response.raise_for_status()
    with open('large-file.zip', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
```

## 錯誤處理

```python
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

try:
    response = requests.get('https://www.example.com', timeout=10)
    response.raise_for_status()  # 如果狀態碼是錯誤則拋出例外

except Timeout:
    print("請求超時")
except HTTPError as e:
    print(f"HTTP 錯誤: {e}")
except RequestException as e:
    print(f"請求錯誤: {e}")
```

## 設定超時

```python
import requests

# 設定連線超時和讀取超時
response = requests.get(
    'https://www.example.com',
    timeout=(3.05, 27)  # (連線超時, 讀取超時)
)
```

## 重試機制

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 建立重試策略
retry_strategy = Retry(
    total=3,  # 最多重試 3 次
    backoff_factor=1,  # 重試間隔
    status_forcelist=[429, 500, 502, 503, 504]  # 這些狀態碼會觸發重試
)

# 建立 adapter
adapter = HTTPAdapter(max_retries=retry_strategy)

# 建立 session 並掛載 adapter
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用 session 發送請求
response = session.get('https://www.example.com')
```

## 實戰範例：爬取 Hacker News

```python
import requests
from bs4 import BeautifulSoup

# 發送請求
response = requests.get('https://news.ycombinator.com')

# 檢查是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 取得所有文章標題
    titles = soup.find_all('span', class_='titleline')

    for i, title in enumerate(titles[:10], 1):
        link = title.find('a')
        print(f"{i}. {link.text}")
else:
    print(f"請求失敗: {response.status_code}")
```

## 常用屬性與方法

| 屬性/方法 | 說明 |
|-----------|------|
| `response.text` | 回應內容 (字串) |
| `response.content` | 回應內容 (位元組) |
| `response.json()` | 解析 JSON 回應 |
| `response.status_code` | HTTP 狀態碼 |
| `response.headers` | 回應標頭 |
| `response.cookies` | 回應的 cookies |
| `response.url` | 最終的 URL |
| `response.encoding` | 編碼方式 |
| `response.raise_for_status()` | 如有錯誤則拋出例外 |

## 下一步

學會 Requests 後，接下來學習如何使用 BeautifulSoup 解析 HTML 內容。

---

*參考資源：ScrapingBee, Oxylabs, Real Python (2024-2025)*
