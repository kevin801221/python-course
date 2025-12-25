#!/usr/bin/env python3
"""
從 73.深入浅出pandas-2.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
scores = np.random.randint(60, 101, (5, 3))
courses = ['語文', '數學', '英語']
stu_ids = np.arange(1001, 1006)
df1 = pd.DataFrame(data=scores, columns=courses, index=stu_ids)
df1
# === 範例 2 ===
scores = {
    '語文': [62, 72, 93, 88, 93],
    '數學': [95, 65, 86, 66, 87],
    '英語': [66, 75, 82, 69, 82],
}
stu_ids = np.arange(1001, 1006)
df2 = pd.DataFrame(data=scores, index=stu_ids)
df2
# === 範例 3 ===
df3 = pd.read_csv('data/2018年北京積分落戶資料.csv', index_col='id')
df3
# === 範例 4 ===
df4 = pd.read_excel('data/2022年股票資料.xlsx', sheet_name='AMZN', index_col='Date')
df4
# === 範例 5 ===
import pymysql

# 建立一個MySQL資料庫的連線物件
conn = pymysql.connect(
    host='101.42.16.8', port=3306,
    user='guest', password='Guest.618',
    database='hrs', charset='utf8mb4'
)
# 透過SQL從資料庫二維表讀取資料建立DataFrame
df5 = pd.read_sql('select * from tb_emp', conn, index_col='eno')
df5
# === 範例 6 ===
%pip install sqlalchemy
# === 範例 7 ===
from sqlalchemy import create_engine

# 透過指定的URL（統一資源定位符）訪問資料庫
engine = create_engine('mysql+pymysql://guest:Guest.618@101.42.16.8:3306/hrs')
# 直接透過表名載入整張表的資料
df5 = pd.read_sql('tb_emp', engine, index_col='eno')
df5
# === 範例 8 ===
df6 = pd.read_sql('select dno, dname, dloc from tb_dept', engine, index_col='dno')
df6
# === 範例 9 ===
engine.connect().close()
# === 範例 10 ===
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://guest:Guest.618@101.42.16.8:3306/hrs')
dept_df = pd.read_sql_table('tb_dept', engine, index_col='dno')
emp_df = pd.read_sql_table('tb_emp', engine, index_col='eno')
emp2_df = pd.read_sql_table('tb_emp2', engine, index_col='eno')
# === 範例 11 ===
emp_df.info()
# === 範例 12 ===
emp_df.head()
# === 範例 13 ===
emp_df.ename
# === 範例 14 ===
emp_df['ename']
# === 範例 15 ===
emp_df.iloc[1]
# === 範例 16 ===
emp_df.loc[2056]
# === 範例 17 ===
emp_df[['ename', 'job']]
# === 範例 18 ===
emp_df.loc[[2056, 7800, 3344]]
# === 範例 19 ===
emp_df['job'][2056]
# === 範例 20 ===
emp_df.loc[2056]['job']
# === 範例 21 ===
emp_df.loc[2056, 'job']
# === 範例 22 ===
emp_df.loc[2056, 'job'] = '架構師'
# === 範例 23 ===
emp_df.loc[2056:3344]
# === 範例 24 ===
emp_df[emp_df.sal > 3500]
# === 範例 25 ===
emp_df[(emp_df.sal > 3500) & (emp_df.dno == 20)]
# === 範例 26 ===
emp_df.query('sal > 3500 and dno == 20')
