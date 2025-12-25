#!/usr/bin/env python3
"""
從 85.回归模型.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_csv('https://archive.ics.uci.edu/static/public/9/data.csv')
df.info()
# === 範例 2 ===
# 刪除指定的列
df.drop(columns=['car_name'], inplace=True)
# 計算相關係數矩陣
df.corr()
# === 範例 3 ===
# 刪除有缺失值的樣本
df.dropna(inplace=True)
# 將origin欄位處理為類別型別
df['origin'] = df['origin'].astype('category') 
# 將origin欄位處理為獨熱編碼
df = pd.get_dummies(df, columns=['origin'], drop_first=True)
df
# === 範例 4 ===
from sklearn.model_selection import train_test_split

X, y = df.drop(columns='mpg').values, df['mpg'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)
# === 範例 5 ===
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# === 範例 6 ===
print('迴歸係數:', model.coef_)
print('截距:', model.intercept_)
# === 範例 7 ===
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'均方誤差: {mse:.4f}')
print(f'平均絕對誤差: {mae:.4f}')
print(f'決定係數: {r2:.4f}')
# === 範例 8 ===
from sklearn.linear_model import Ridge

model = Ridge()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('迴歸係數:', model.coef_)
print('截距:', model.intercept_)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'均方誤差: {mse:.4f}')
print(f'決定係數: {r2:.4f}')
# === 範例 9 ===
from sklearn.linear_model import Lasso

model = Lasso()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('迴歸係數:', model.coef_)
print('截距:', model.intercept_)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'均方誤差: {mse:.4f}')
print(f'決定係數: {r2:.4f}')
# === 範例 10 ===
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

# 對特徵進行選擇和標準化處理
scaler = StandardScaler()
scaled_X = scaler.fit_transform(X[:, [1, 2, 3, 5]])
# 重新拆分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, train_size=0.8, random_state=3)

# 模型的建立、訓練和預測
model = SGDRegressor()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('迴歸係數:', model.coef_)
print('截距:', model.intercept_)

# 模型評估
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'均方誤差: {mse:.4f}')
print(f'決定係數: {r2:.4f}')
# === 範例 11 ===
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 6, 150)
y = x ** 2 - 4 * x + 3 + np.random.normal(1, 1, 150)
plt.scatter(x, y)
plt.show()
# === 範例 12 ===
r2 = r2_score(y, y_pred)
print(f'決定係數: {r2:.4f}')
# === 範例 13 ===
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2)
x_ = poly.fit_transform(x_)

model = LinearRegression()
model.fit(x_, y)
y_pred = model.predict(x_)
r2 = r2_score(y, y_pred)
print(f'決定係數: {r2:.4f}')
# === 範例 14 ===
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 生成1000條樣本資料，每個樣本包含6個特徵
X, y = make_classification(n_samples=1000, n_features=6, random_state=3)
# 將1000條樣本資料拆分為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 建立和訓練邏輯迴歸模型
model = LogisticRegression()
model.fit(X_train, y_train)

# 對測試集進行預測並評估
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
