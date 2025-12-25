#!/usr/bin/env python3
"""
從 如何快速驾驭 pandas 库.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
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
# === 範例 2 ===
pd.read_excel(
    io,           # 工作簿檔案的路徑
    sheet_name,   # 工作表的名字
    skip_footer,  # 跳過末尾多少行
)
# === 範例 3 ===
pd.read_sql(
    sql,          # SQL查詢或二維表的名字
    con,          # 資料庫連線
    parse_dates,  # 指定需要解析成日期的列
    index_col,    # 指定索隱裂
    columns,      # 需要載入的列
    chunksize,    # 載入資料的體量
    dtype,        # 指定列的資料型別
)
# === 範例 4 ===
pd.DataFrame(data=[[95, 87], [66, 78], [92, 89]], index=[1001, 1002, 1003], columns=['Verbal', 'Math'])
pd.DataFrame(data={'Verbal': [95, 66, 92], 'Math': [87, 78, 89]}, index=[1001, 1002, 1003])
# === 範例 5 ===
df.info()
# === 範例 6 ===
df.head(10)
df.tail(5)
# === 範例 7 ===
df['column_name']
df.colume_name
# === 範例 8 ===
df.loc['row_index']
df.iloc[0]
# === 範例 9 ===
df.at['row_index', 'column_name']
df.iat[0, 0]
# === 範例 10 ===
df.drop(
    labels,   # 要刪除的行或列的索引
    axis,     # axis=0，labels表示行索引；axis=1，labels表示列索引
    index,    # 要刪除的行的索引
    columns,  # 要刪除的列的索引
    inplace,  # 是否就地刪除（inplace=True，表示就地刪除不返回新DataFrame物件）
)
# === 範例 11 ===
df.query(expr)  # 透過表示式指定篩選條件
df[bool_index]  # 布林索引
# === 範例 12 ===
df.sampe(
    n,             # 樣本容量
    frac,          # 抽樣比例
    replace,       # 有放回或無放回抽樣（預設值False）
    random_state,  # 隨機數種子（種子相同每次抽樣的結果相同）
)
# === 範例 13 ===
df.reset_index(
    level,    # 對於多級索引指定重置哪一級的索引
    drop,     # 是否丟棄索引（drop=False表示索引會被處理成普通列）
    inplace,  # 是否就地處理（要不要返回新的DataFrame物件）
)
# === 範例 14 ===
df.set_index(
   keys,              # 指定作為索引的列
   drop,              # 是否刪除作為索引的列（預設值True）
   append,            # 是否將指定列加入現有的索引（預設值False）
   inplace,           # 是否就地處理（要不要返回新的DataFrame物件）
   verify_integrity,  # 檢查索引列是否存在重複值（預設值False）
)
# === 範例 15 ===
df.reindex()
df[fancy_index]       # 花式索引
df.loc[facy_index]    # 花式索引
df.iloc[fancy_index]  # 花式索引
# === 範例 16 ===
df.sort_index(
    axis,         # 確定行索引或列索引（預設值0）
    level,        # 對於多級索引指定索引的級別
    ascending,    # 升序或降序（預設值True）
    inplace,      # 是否就地排序
    kind,         # 排序演算法（預設值'quicksort'）
    na_position,  # 空值放在最前還是最後（預設值'last'）
    key,          # 傳入比較索引大小的函式（自定義比較規則）
)
# === 範例 17 ===
pd.concat(
    objs,          # 儲存多個DataFrame物件的容器
    axis,          # 沿著哪個軸進行拼接
    ignore_index,  # 是否忽略原來的索引（預設值False）
)
# === 範例 18 ===
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
# === 範例 19 ===
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
# === 範例 20 ===
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
# === 範例 21 ===
# 替換異常值
df.replace(
    to_replace,  # 被替換的值
    value,       # 替換的值
    inplace,     # 是否就地替換（要不要返回新的DataFrame物件）
    regex,       # 是否啟動正規表示式替換（預設值False）
)
# === 範例 22 ===
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
# === 範例 23 ===
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
# === 範例 24 ===
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
# === 範例 25 ===
pd.get_dummies(
    data,        # 需要轉換為虛擬變數的Series或DataFrame
    prefix,      # 指定生成的虛擬變數列的字首
    prefix_sep,  # 字首和列名之間的分隔符
    dummy_na,    # 是否為空值（NaN）生成一個列（預設值False）
    columns,     # 指定要轉換的列名
    drop_first,  # 是否從生成的虛擬變數中刪除第一個類別的列（預設值False）
)
# === 範例 26 ===
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
# === 範例 27 ===
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
# === 範例 28 ===
s.mean()     # 均值
s.median()   # 中位數
s.mode()     # 眾數
s.max()      # 最大值
s.min()      # 最小值
s.var(ddof)  # 方差（ddof代表自由度校正值）
s.std(ddof)  # 標準差（ddof代表自由度校正值）
s.skew()     # 偏態係數
s.kurt()     # 峰度係數
# === 範例 29 ===
df.cov()         # 協方差
df.corr(method)  # 相關係數（預設'pearson'表示皮爾遜相關係數，可選值還有'kendall'和'spearman'）
# === 範例 30 ===
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
# === 範例 31 ===
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
# === 範例 32 ===
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
# === 範例 33 ===
pd.crosstab(
    index,         # 交叉表中的行變數
    columns,       # 交叉表中的列變數
    values,        # 用於填充交叉表的值（可選項）
    aggfunc,       # 聚合函式（可選項）
    margins,       # 是否計算行列總計（預設值False）
    margins_name,  # 總計列的名字（預設值'All'）
)
# === 範例 34 ===
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
