# Selenium 動態網頁爬取教學

> 處理 JavaScript 渲染的網頁

## 什麼是 Selenium?

Selenium 是一個瀏覽器自動化工具，可以控制真實的瀏覽器執行各種操作。在網頁爬蟲中，Selenium 主要用於處理需要 JavaScript 渲染的動態網頁。

### 為什麼需要 Selenium?

- **JavaScript 渲染**：許多現代網站使用 JavaScript 動態載入內容
- **模擬使用者行為**：點擊、滾動、輸入文字等
- **處理登入**：自動化登入流程
- **繞過反爬蟲**：模擬真實瀏覽器行為

## 安裝 Selenium

```bash
# 使用 uv (推薦)
uv pip install selenium

# 或使用 pip
pip install selenium
```

### 關於 WebDriver

Selenium 4.6+ 版本開始自動管理 WebDriver，不需要手動下載。如果遇到問題，可以使用 `webdriver-manager`：

```bash
uv pip install webdriver-manager
```

## 基本使用

### 啟動瀏覽器

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 設定 Chrome 選項
options = Options()
options.add_argument('--headless')  # 無頭模式 (不顯示瀏覽器視窗)
options.add_argument('--window-size=1920,1080')

# 啟動 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)

# 開啟網頁
driver.get('https://www.example.com')

# 取得頁面內容
print(driver.page_source)

# 關閉瀏覽器
driver.quit()
```

### 使用 Firefox

```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.get('https://www.example.com')
driver.quit()
```

## 定位元素

Selenium 提供多種方式來定位頁面元素：

```python
from selenium.webdriver.common.by import By

# 透過 ID
element = driver.find_element(By.ID, 'element-id')

# 透過 Class Name
elements = driver.find_elements(By.CLASS_NAME, 'class-name')

# 透過 CSS 選擇器 (推薦)
element = driver.find_element(By.CSS_SELECTOR, 'div.content > p')

# 透過 XPath (強大但複雜)
element = driver.find_element(By.XPATH, '//div[@class="content"]/p')

# 透過 Name 屬性
element = driver.find_element(By.NAME, 'username')

# 透過標籤名稱
elements = driver.find_elements(By.TAG_NAME, 'a')

# 透過連結文字
element = driver.find_element(By.LINK_TEXT, '點擊這裡')
element = driver.find_element(By.PARTIAL_LINK_TEXT, '點擊')
```

## 與元素互動

### 點擊、輸入、送出

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 找到輸入框並輸入文字
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('Python 爬蟲')
search_box.send_keys(Keys.RETURN)  # 按 Enter 鍵

# 點擊按鈕
button = driver.find_element(By.CSS_SELECTOR, 'button.submit')
button.click()

# 清除輸入框
search_box.clear()
```

### 取得元素資訊

```python
element = driver.find_element(By.ID, 'title')

# 取得文字內容
print(element.text)

# 取得屬性值
print(element.get_attribute('href'))
print(element.get_attribute('class'))

# 檢查元素狀態
print(element.is_displayed())  # 是否可見
print(element.is_enabled())    # 是否啟用
print(element.is_selected())   # 是否選中 (用於 checkbox)
```

## 等待機制

### 隱式等待 (Implicit Wait)

```python
# 設定全域等待時間
driver.implicitly_wait(10)  # 最多等待 10 秒
```

### 顯式等待 (Explicit Wait) - 推薦

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 等待特定元素出現
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, 'dynamic-content'))
)

# 等待元素可點擊
element = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.submit'))
)

# 等待元素可見
element = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'result'))
)
```

### 常用的等待條件

| 條件 | 說明 |
|------|------|
| `presence_of_element_located` | 元素存在於 DOM 中 |
| `visibility_of_element_located` | 元素可見 |
| `element_to_be_clickable` | 元素可點擊 |
| `text_to_be_present_in_element` | 元素包含特定文字 |
| `title_contains` | 標題包含特定文字 |
| `url_contains` | URL 包含特定文字 |

## 處理彈出視窗與框架

### Alert 對話框

```python
from selenium.webdriver.common.alert import Alert

# 等待 Alert 出現
alert = wait.until(EC.alert_is_present())

# 取得 Alert 文字
print(alert.text)

# 接受 (按確定)
alert.accept()

# 取消 (按取消)
alert.dismiss()

# 輸入文字 (如果是 prompt)
alert.send_keys('輸入的文字')
```

### iframe 框架

```python
# 切換到 iframe
driver.switch_to.frame('iframe-name')  # 透過名稱
driver.switch_to.frame(0)  # 透過索引
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe'))

# 切回主框架
driver.switch_to.default_content()
```

### 新視窗/分頁

```python
# 取得目前視窗
original_window = driver.current_window_handle

# 點擊連結開啟新視窗
driver.find_element(By.LINK_TEXT, '開啟新視窗').click()

# 切換到新視窗
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# 切回原視窗
driver.switch_to.window(original_window)
```

## 捲動頁面

```python
from selenium.webdriver.common.action_chains import ActionChains

# 捲動到底部
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 捲動到特定元素
element = driver.find_element(By.ID, 'target')
driver.execute_script("arguments[0].scrollIntoView();", element)

# 捲動特定距離
driver.execute_script("window.scrollBy(0, 500);")
```

## 截圖

```python
# 整個頁面截圖
driver.save_screenshot('screenshot.png')

# 特定元素截圖
element = driver.find_element(By.ID, 'chart')
element.screenshot('element.png')
```

## 執行 JavaScript

```python
# 執行 JavaScript
result = driver.execute_script("return document.title;")
print(result)

# 修改頁面內容
driver.execute_script("document.body.style.zoom = '80%';")

# 取得隱藏元素的資料
data = driver.execute_script("""
    return document.querySelector('script#__NEXT_DATA__').textContent;
""")
```

## 實戰範例：爬取動態網頁

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 設定無頭模式
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

driver = webdriver.Chrome(options=options)

try:
    # 開啟網頁
    driver.get('https://example.com/products')

    # 等待產品列表載入
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card')))

    # 捲動載入更多內容
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # 使用 BeautifulSoup 解析
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = soup.find_all('div', class_='product-card')

    for product in products:
        title = product.find('h3').text.strip()
        price = product.find('span', class_='price').text.strip()
        print(f"{title}: {price}")

finally:
    driver.quit()
```

## 效能優化建議

1. **使用無頭模式**：減少資源消耗
2. **停用圖片載入**：加快頁面載入速度
3. **使用顯式等待**：避免不必要的等待時間
4. **重用瀏覽器實例**：減少啟動開銷

### 停用圖片載入

```python
options = Options()
options.add_argument('--headless')

# 停用圖片
prefs = {'profile.managed_default_content_settings.images': 2}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)
```

## 替代方案：Playwright

Playwright 是 Microsoft 開發的現代瀏覽器自動化工具，語法更簡潔：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    page.screenshot(path='screenshot.png')
    browser.close()
```

## 下一步

學會 Selenium 後，接下來學習 Scrapy 框架來建立大規模爬蟲專案。

---

*參考資源：ScrapingBee, Oxylabs, Real Python (2024-2025)*
