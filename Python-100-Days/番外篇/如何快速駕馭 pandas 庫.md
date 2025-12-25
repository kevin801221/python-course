## 如何快速駕馭 pandas 庫

最近有小夥伴提到，Python 做資料分析的 pandas 庫函式和方法實在太多，感覺學習和使用起來思路都非常混亂。之前回復過這個問題，今天把它更系統的整理一下，畢竟這個庫是 Python 資料科學生態圈中扮演著極為重要的角色，雖然目前有很多 pandas 庫的替代品（如：polars、cuDF等），但是使用方法跟 pandas 可以說是大同小異。

### 三個核心類

Pandas 庫有三個最核心的類，其中最重要的是`DataFrame`型別，它是學習的重點，如下圖所示。

<img src="res/pandas_data_structures.png" style="zoom:50%;">

1. `Series`：表示一維資料，跟一維陣列類似（帶標籤的陣列），每個資料都有自己的索引（標籤），可以透過索引訪問資料。
2. `DataFrame`：表示二維資料，類似於 Excel 電子表格，行和列都有自己的索引（標籤），可以透過索引訪問行、列、單元格。
3. `Index`：表示索引，為`Series`和`DataFrame` 提供索引服務，`Index`有很多的子型別，適用於需要不同型別的索引的場景。

### 資料分析流程

學習和使用 pandas 重點是`DataFrame`的應用，我們建議大家按照資料分析的流程來掌握對應的函式和方法，這樣做往往會事半功倍。資料分析流程如下圖所示，其中藍色虛線圈中的部分就是可以透過 BI 工具（如：Power BI、Tableau等）或 Python 程式來完成的部分。

<img src="res/data_analysis_steps.png" style="zoom:38%;">

#### 資料獲取

資料獲取也可以稱為資料載入，其本質就是建立`DataFrame`物件，需要掌握以下幾個函式：

1. 從 CSV 檔案載入資料。

```python
pd.read_csv(
    filepath,      # CSV檔案路徑（可以本地絕對路徑或相對路徑，也可以是一個URL）
    sep,           # 欄位分隔符（預設是逗號）
    header,        # 表頭在第幾行
    encoding,      # 檔案編碼（預設utf-8）
    quotechar,     # 包裹字串的符號（預設是雙引號）
    usecols,       # 載入哪些列
    index_col,     # 指定索引列
    dtype,         # 指定列的資料型別
    converters,    # 指定列的資料轉換器
    nrows,         # 載入多少行資料
    skiprows,      # 指定需要跳過的行
    parse_dates,   # 將哪些列解析為日期時間
    date_format,   # 日期格式
    true_values,   # 被視為布林值True的值
    false_values,  # 被視為布林值False的值
    na_values,     # 被視為空值的值
    na_filter,     # 是否檢測空值標記
    on_bad_lines,  # 遇到有問題的行如何處理（可選項：'error'、'warn'、'skip'）
    engine,        # 指定底層引擎（例如：可以使用更快的Arrow引擎來處理體量更大的資料）
    iterator,      # 是否開啟迭代器模式（處理大資料時減少記憶體開銷）
    chunksize,     # 迭代器模式下每次載入數量的體量
)
```

2. 從 Excel 檔案載入資料。

```python
pd.read_excel(
    io,           # 工作簿檔案的路徑
    sheet_name,   # 工作表的名字
    skip_footer,  # 跳過末尾多少行
)
```

> **說明**：`read_excel`函式跟`read_csv`有很多作用相同的引數，這裡就沒有贅述了。從 Excel 檔案中載入資料時，沒有迭代器模式。

3. 從資料庫或數倉載入資料。

```python
pd.read_sql(
    sql,          # SQL查詢或二維表的名字
    con,          # 資料庫連線
    parse_dates,  # 指定需要解析成日期的列
    index_col,    # 指定索隱裂
    columns,      # 需要載入的列
    chunksize,    # 載入資料的體量
    dtype,        # 指定列的資料型別
)
```

4. 其他建立`DataFrame`物件的方式。

```python
pd.DataFrame(data=[[95, 87], [66, 78], [92, 89]], index=[1001, 1002, 1003], columns=['Verbal', 'Math'])
pd.DataFrame(data={'Verbal': [95, 66, 92], 'Math': [87, 78, 89]}, index=[1001, 1002, 1003])
```

如果要對`DataFrame`中的資料或索引進行操作，需要掌握下面的運算和方法。

1. 檢視資訊

```python
df.info()
```

2. 檢視前/後 N 行

```python
df.head(10)
df.tail(5)
```

3. 操作列

```python
df['column_name']
df.colume_name
```

4. 操作行

```python
df.loc['row_index']
df.iloc[0]
```

5. 操作單元格

```python
df.at['row_index', 'column_name']
df.iat[0, 0]
```

6. 刪除行或列

```python
df.drop(
    labels,   # 要刪除的行或列的索引
    axis,     # axis=0，labels表示行索引；axis=1，labels表示列索引
    index,    # 要刪除的行的索引
    columns,  # 要刪除的列的索引
    inplace,  # 是否就地刪除（inplace=True，表示就地刪除不返回新DataFrame物件）
)
```

7. 篩選資料

```python
df.query(expr)  # 透過表示式指定篩選條件
df[bool_index]  # 布林索引
```

8. 隨機抽樣

```python
df.sampe(
    n,             # 樣本容量
    frac,          # 抽樣比例
    replace,       # 有放回或無放回抽樣（預設值False）
    random_state,  # 隨機數種子（種子相同每次抽樣的結果相同）
)
```

9. 重置索引

```python
df.reset_index(
    level,    # 對於多級索引指定重置哪一級的索引
    drop,     # 是否丟棄索引（drop=False表示索引會被處理成普通列）
    inplace,  # 是否就地處理（要不要返回新的DataFrame物件）
)
```

10. 設定索引

```python
df.set_index(
   keys,              # 指定作為索引的列
   drop,              # 是否刪除作為索引的列（預設值True）
   append,            # 是否將指定列加入現有的索引（預設值False）
   inplace,           # 是否就地處理（要不要返回新的DataFrame物件）
   verify_integrity,  # 檢查索引列是否存在重複值（預設值False）
)
```

11. 調整索引順序

```python
df.reindex()
df[fancy_index]       # 花式索引
df.loc[facy_index]    # 花式索引
df.iloc[fancy_index]  # 花式索引
```

12. 索引排序

```python
df.sort_index(
    axis,         # 確定行索引或列索引（預設值0）
    level,        # 對於多級索引指定索引的級別
    ascending,    # 升序或降序（預設值True）
    inplace,      # 是否就地排序
    kind,         # 排序演算法（預設值'quicksort'）
    na_position,  # 空值放在最前還是最後（預設值'last'）
    key,          # 傳入比較索引大小的函式（自定義比較規則）
)
```


#### 資料重塑

1. 拼接（類似於 SQL 中的 union 操作）

```python
pd.concat(
    objs,          # 儲存多個DataFrame物件的容器
    axis,          # 沿著哪個軸進行拼接
    ignore_index,  # 是否忽略原來的索引（預設值False）
)
```

2. 合併（類似於 SQL 中的 join 操作）

```python
pd.merge(
    left,         # 左表
    right,        # 右表
    how,          # 指定連表的方式（預設值'inner'表示內連線）
    on,           # 指定連表欄位（如果左右兩表連表欄位同名）
    left_on,      # 指定左表的連表欄位
    right_on,     # 指定右表的連表欄位
    left_index,   # 是否使用左表的索引連表
    right_index,  # 是否使用右表的索引連表
    suffixes,     # 指定同名列的字尾（預設值('_x', '_y')）
)
```


#### 資料清洗

1. 缺失值

```python
# 甄別缺失值
df.isna()
df.notna()
# 刪除缺失值
df.dropna(
    axis,     # 刪行或刪列（預設值0）
    how,      # 是否存在任意一個缺失值就刪除（預設值'any'）
    subset,   # 只對哪些行或列刪除空值
    inplace,  # 是否就地刪除（要不要返回新的DataFrame物件）
)
# 填充缺失值
df.fillna(
    value,    # 填充的值
    method,   # 填充空值的方法
    inplace,  # 是否就地填充（要不要返回新的DataFrame物件）
)
# 使用插值演算法插值
df.interpolate(
    method,   # 插值演算法（預設值'linear'表示線性插值法） 
    axis,     # 沿著哪個軸插值
    inplace,  # 是否就地插值（要不要返回新的DataFrame物件）
)
```

2. 重複值

```python
# 甄別重複值
df.duplicated(
    subset,   # 用於判斷重複的列標籤
    keep,     # 如何處理重複項（預設值'first'表示保留第一項）
)
# 刪除重複值
df.drop_duplicates(
    subset,   # 用於判斷重複的列標籤
    keep,     # 如何處理重複項（預設值'first'表示保留第一項）
    inplace,  # 是否就地去重（預設值False）
)
# 統計非重複值
df.nunique(axis)
```

3. 異常值

異常值的處理重點在甄別，可以使用數值判定法、z-score 判定法、孤立森林等方法來進行甄別離群點，然後結合實際業務意義判定是不是異常值。對於異常值的處理，通常是替換或刪除，刪除可以用之前提到的`drop`方法刪行或者刪列。

```python
# 替換異常值
df.replace(
    to_replace,  # 被替換的值
    value,       # 替換的值
    inplace,     # 是否就地替換（要不要返回新的DataFrame物件）
    regex,       # 是否啟動正規表示式替換（預設值False）
)
```

4. 預處理

預處理通常在`Series`物件上對資料進行操作，假設變數`s`是一個`Series`物件，具體的操作包括：

- 日期時間預處理

```python
s.dt.year                   # 年
s.dt.quarter                # 季度
s.dt.month                  # 月
s.dt.day                    # 日
s.dt.hour                   # 時
s.dt.minute                 # 分
s.dt.second                 # 秒
s.dt.weekday                # 星期幾
s.dt.to_period(freq)        # 以特定頻率轉換
s.dt.floor(freq)            # 下取整
s.dt.ceil(freq)             # 上取整
s.dt.round(freq)            # 舍入
s.dt.strftime(date_format)  # 格式化
s.dt.tz_localize(tz)        # 時區本地化
s.dt.tz_convert(tz)         # 轉換時區
```

- 字串預處理

```python
s.str.lower()       # 字串變小寫
s.str.upper()       # 字串變大寫
s.str.title()       # 字串首字母大寫
# 字串拆分
s.str.split(
    pat,            # 拆分字元或正規表示式
    n,              # 最大拆分次數
    expand,         # 是否將拆分後的內容展開成多個列（預設值False）
)
# 從字串中捕獲內容
s.str.extract(
    pat,            # 正規表示式
    flags,          # 正規表示式處理標記
    expand,         # 是否將捕獲內容展開成多個列（預設值True）
)
s.str.isalpha()     # 檢查字串是不是字母
s.str.isnumeric()   # 檢查字串是不是數值
s.str.isalnum()     # 檢查字串是不是字母數字
s.str.isspace()     # 檢查字串是不是空白字元
s.str.startswith()  # 檢查字串是否以指定內容開頭 
s.str.endswith()    # 檢查字串是否以指定內容結尾
# 檢查字串是否跟正規表示式匹配
s.str.match(
    pat,            # 正規表示式
    flags,          # 正規表示式處理標記
)
# 檢查字串是否包含指定內容
s.str.contains(
    pat,            # 字串或正規表示式
    flags,          # 正規表示式處理標記
    regex,          # 是否使用正規表示式（預設值True）
)
# 替換
s.str.replace(
    pat,            # 被替換的內容（字串或正規表示式）
    repl,           # 替換的內容
    n,              # 最大替換次數（預設值-1表示全部替換）
    flags,          # 正規表示式處理標記
    regex,          # 是否使用正規表示式（預設值True）
)
s.str.strip()       # 去掉字串多餘的空格
s.str.join(sep)     # 用指定的分隔符將內容拼接成字串
# 字串拼接
s.str.cat(
    others,         # 拼接的內容
    sep,            # 分隔符
    na_rep,         # 空值的替代符
)
s.str.len()         # 獲得字串長度
# 查詢子串的位置
s.str.find(
    sub,            # 子串
    start,          # 起始位置
    end,            # 結束位置
)
```

- 類別預處理

```python
# 類別重排序
s.cat.reorder_categories(
    new_categories,  # 新的類別順序
    inplace,         # 是否就地處理（預設值False）
)
# 新增類別
s.cat.add_categories(
    new_categories,  # 要新增的新類別
    inplace,         # 是否就地處理（預設值False）
)
# 移除類別
s.cat.remove_categories(
    removals,        # 要移除的類別
    inplace,         # 是否就地處理（預設值False）
)
# 移除沒有使用的類別
s.cat.remove_unused_categories(
    inplace,         # 是否就地處理（預設值False）
)
# 類別重新命名
s.cat.rename_categories(
    new_categories,  # 新的類別名稱
    inplace,         # 是否就地處理（預設值False）
)
```

- 二值化（虛擬變數）

```python
pd.get_dummies(
    data,        # 需要轉換為虛擬變數的Series或DataFrame
    prefix,      # 指定生成的虛擬變數列的字首
    prefix_sep,  # 字首和列名之間的分隔符
    dummy_na,    # 是否為空值（NaN）生成一個列（預設值False）
    columns,     # 指定要轉換的列名
    drop_first,  # 是否從生成的虛擬變數中刪除第一個類別的列（預設值False）
)
```

- 離散化（分箱）

```python
pd.cut(
    x,        # 要分割的輸入資料（一維資料）
    bins,     # 分割的區間數或具體的區間邊界
    right,    # 區間是否包含右端點（預設值False）
    labels,   # 指定每個區間的標籤
    retbins,  # 是否返回分割的邊界陣列（預設值False）
    ordered,  # 返回的類別是否是有序的（預設值True）
)
pd.qcut(
    x,        # 要分割的輸入資料（一維資料）
    q,        # 分割點的數量或具體的分位數
    labels,   # 指定每個區間的標籤
    retbins,  # 是否返回分割的邊界陣列（預設值False）
)
```

- 自定義轉換

```python
s.map(arg)          # 對資料進行元素級別的轉換和對映
df.map(func)        # 對資料進行元素級別的轉換和對映
# 透過指定函式對資料進行元素級別的轉換
s.apply(
    func,           # 作用於每個元素的函式
    convert_type,   # 嘗試將結果轉換為最適合的型別（預設值True）
    args,           # 傳遞給func的額外位置引數
    kwargs,         # 傳遞給func的額外關鍵字引數
)   
# 透過指定函式對資料進行行級或列級的轉換
df.apply(
    func,           # 作用域行或列的函式
    axis,           # 控制做行級還是列級轉換
    result_type,    # 指定返回的型別（'expand'表示擴充套件為列，'reduce'表示返回標量，'broadcast'表示廣播為原始形狀）
    args,           # 傳遞給func的額外位置引數
    kwargs,         # 傳遞給func的額外關鍵字引數
)
s.transform(func)   # 透過指定一個或多個函式對資料進行元素級別的轉換
df.transform(func)  # 透過指定一個或多個函式對資料進行行級或列級轉換
```

#### 資料透視

1. 描述性統計資訊

```python
s.mean()     # 均值
s.median()   # 中位數
s.mode()     # 眾數
s.max()      # 最大值
s.min()      # 最小值
s.var(ddof)  # 方差（ddof代表自由度校正值）
s.std(ddof)  # 標準差（ddof代表自由度校正值）
s.skew()     # 偏態係數
s.kurt()     # 峰度係數
```

2. 相關性分析

```python
df.cov()         # 協方差
df.corr(method)  # 相關係數（預設'pearson'表示皮爾遜相關係數，可選值還有'kendall'和'spearman'）
```

3. 排序和頭部值

```python
# 排序
s.sort_values(
    asending,     # 升序或降序（預設值True）
    inplace,      # 是否就地排序（預設值False）
    kind,         # 排序演算法（預設值'quicksort'）
    na_position,  # 空值的位置（預設值'last'）
    key,          # 指定比較元素的規則（函式）
)
# 排序
df.sort_values(
    by,           # 排序的依據
    ascending,    # 升序或降序（預設值True）
    inplace,      # 是否就地排序（預設值False）
    kind,         # 排序演算法（預設值'quicksort'）
    na_position,  # 空值的位置（預設值'last'）
    key,          # 指定比較元素的規則（函式）
)
# TopN元素（頭部）
s.nlargest(
    n,            # 前N個最大值
    keep,         # 如何處理重複值（預設值'first'）
)
# TopN元素（頭部）
df.nlargest(
    n,            # 前N個最大值
    columns,      # 指定用於排序的列名
    keep,         # 如何處理重複值（預設值'first'）
)
# TopN元素（尾部）
s.nsmallest(
    n,            # 前N個最小值
    keep,         # 如何處理重複值（預設值'first'）
)
# TopN元素（尾部）
df.nsmallest(
    n,            # 前N個最小值
    columns,      # 指定用於排序的列名
    keep,         # 如何處理重複值（預設值'first'）
)
```

4. 分組聚合

```python
df.groupby(
    by,          # 指定用於分組的列名
    level,       # 對於多級索引指定用哪一級分組
    as_index,    # 是否將分組的列設定為索引（預設值True）
    sort,        # 是否對分組的結果進行排序（預設值True）
    observed,    # 只考慮在資料中實際出現的分組（預設值False）
).aggregate(
    func,        # 單個函式或函式列表
    args,       # 函式的可變引數
    kwargs,    # 函式的關鍵字引數
)
df.pivot(
    index,       # 指定用作索引的列
    columns,     # 要作為新列的列 
    values,      # 用於填充新DataFrame中的值的列
)
df.melt(
    id_vars,     # 在轉換過程中保持不變的列
    value_vars,  # 要轉換為行的列
    var_name,    # 指定儲存原列名的新列名
    value_name,  # 指定儲存原資料值的新列名
)
```

5. 透視表

```python
pd.pivot_table(
    data,          # DataFrame物件
    values,        # 需要聚合的列
    index,         # 分組資料的欄位（行索引）
    columns,       # 分組資料的欄位（列索引）
    aggfunc,       # 聚合函式（預設值'mean'）
    fill_value,    # 填充空值的值
    margins,       # 是否計算行列總計（預設值False）
    margins_name,  # 總計列的名字（預設值'All'）
    observed       # 只考慮在資料中實際出現的分組（預設值False）
)
```

6. 交叉表

```python
pd.crosstab(
    index,         # 交叉表中的行變數
    columns,       # 交叉表中的列變數
    values,        # 用於填充交叉表的值（可選項）
    aggfunc,       # 聚合函式（可選項）
    margins,       # 是否計算行列總計（預設值False）
    margins_name,  # 總計列的名字（預設值'All'）
)
```

#### 資料呈現

```python
df.plot(
    figsize,   # 圖表尺寸（二元組）
    kind,      # 圖表型別
    ax,        # 繪圖的座標系
    x,         # 橫軸資料
    y,         # 縱軸資料
    title,     # 圖表標題
    grid,      # 是否繪製網格
    legend,    # 是否顯示圖例
    xticks,    # 橫軸刻度
    yticks,    # 縱軸刻度
    xlim,      # 橫軸取值範圍
    ylim,      # 縱軸取值範圍
    xlabel,    # 橫軸標籤
    ylabel,    # 縱軸標籤
    rot,       # 軸標籤旋轉角度
    fontsize,  # 軸標籤字型大小
    colormap,  # 顏色系列
    stacked,   # 是否繪製堆疊圖（預設值False）
    colorbar,  # 是否顯示色彩條
)
```

`plot`方法最重要的引數是`kind`，它可以控制圖表的型別，具體如下所示：

1. 折線圖：`kind='line'`
2. 散點圖：`kind='scatter'`
3. 柱狀圖：`kind='bar'`
4. 條狀圖（水平柱狀圖）：`kind='barh'`
5. 餅狀圖：`kind='pie'`
6. 直方圖：`kind='hist'`
7. 箱線圖：`kind='box'`
8. 面積圖：`kind='area'`
9. 核密度估計圖：`kind='kde'`

### 總結

大家可以找一個資料集按照上面講解的流程把這些最常用的型別、函式和方法過一遍，是不是印象就深刻一點了。更詳細的內容還是推薦閱讀我的專欄[《基於Python的資料分析》](https://www.zhihu.com/column/c_1217746527315496960)或者觀看B站上的影片[《Python資料分析三劍客》](https://www.bilibili.com/video/BV13t4y1a7TV/)。