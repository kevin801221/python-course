#!/usr/bin/env python3
"""
從 76.深入浅出pandas-5.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
sales_df = pd.read_excel('data/2020年銷售資料.xlsx')
sales_df['月份'] = sales_df.銷售日期.dt.month
sales_df['銷售額'] = sales_df.售價 * sales_df.銷售數量
result_df = sales_df.pivot_table(index='月份', values='銷售額', aggfunc='sum')
result_df.rename(columns={'銷售額': '本月銷售額'}, inplace=True)
result_df
# === 範例 2 ===
result_df['上月銷售額'] = result_df.本月銷售額.shift(1)
result_df
# === 範例 3 ===
result_df['環比'] = (result_df.本月銷售額 - result_df.上月銷售額) / result_df.上月銷售額
result_df.style.format(
    formatter={'上月銷售額': '{:.0f}', '環比': '{:.2%}'},
    na_rep='--------'
)
# === 範例 4 ===
result_df.drop(columns=['上月銷售額', '環比'], inplace=True)
# === 範例 5 ===
result_df['環比'] = result_df.pct_change()
result_df
# === 範例 6 ===
boston_df = pd.read_csv('data/boston_house_price.csv')
boston_df
