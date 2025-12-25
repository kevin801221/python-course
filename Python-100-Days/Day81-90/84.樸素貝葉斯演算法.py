#!/usr/bin/env python3
"""
從 84.朴素贝叶斯算法.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)
# === 範例 2 ===
import numpy as np
import pandas as pd


def naive_bayes_fit(X, y):
    """
    :param X: 樣本特徵
    :param Y: 樣本標籤
    :returns: 二元組 - (先驗機率, 似然性)
    """
    # 計算先驗機率
    clazz_labels, clazz_counts = np.unique(y, return_counts=True)
    prior_probs = pd.Series({k: v / y.size for k, v in zip(clazz_labels, clazz_counts)})
    # 複製陣列建立副本
    X = np.copy(X)
    # 儲存似然性計算結果的字典
    likelihoods = {}
    for j in range(X.shape[1]):  # 對特徵的迴圈
        # 對特徵進行等寬分箱（離散化處理）
        X[:, j] = pd.cut(X[:, j], bins=5, labels=np.arange(1, 6))
        for i in prior_probs.index:
            # 按標籤類別拆分資料並統計每個特徵值出現的頻次
            x_prime = X[y == i, j]
            x_values, x_counts = np.unique(x_prime, return_counts=True)
            for k, value in enumerate(x_values):  # 對不同特徵值的迴圈
                # 計算似然性並儲存在字典中（字典的鍵是一個三元組 - (標籤, 特徵序號, 特徵值)）
                likelihoods[(i, j, value)] = x_counts[k] / x_prime.size
    return prior_probs, likelihoods
# === 範例 3 ===
p_ci, p_x_ci = naive_bayes_fit(X_train, y_train)
print('先驗機率: ', p_ci, sep='\n')
print('似然性: ', p_x_ci, sep='\n')
# === 範例 4 ===
def naive_bayes_predict(X, p_ci, p_x_ci):
    """
    樸素貝葉斯分類器預測
    :param X: 樣本特徵
    :param p_ci: 先驗機率
    :param p_x_ci: 似然性
    :return: 預測的標籤
    """
    # 對特徵進行等寬分箱（離散化處理）
    X = np.copy(X)
    for j in range(X.shape[1]):
        X[:, j] = pd.cut(X[:, j], bins=5, labels=np.arange(1, 6))
    # 儲存每個樣本對應每個類別後驗機率的二維陣列
    results = np.zeros((X.shape[0], p_ci.size))
    clazz_labels = p_ci.index.values
    for k in range(X.shape[0]):
        for i, label in enumerate(clazz_labels):
            # 獲得先驗機率（訓練的結果）
            prob = p_ci.loc[label]
            # 計算獲得特徵資料後的後驗機率
            for j in range(X.shape[1]):
                # 如果沒有對應的似然性就取值為0
                prob *= p_x_ci.get((i, j, X[k, j]), 0)
            results[k, i] = prob
    # 根據每個樣本對應類別最大的機率選擇預測標籤
    return clazz_labels[results.argmax(axis=1)]
# === 範例 5 ===
y_pred = naive_bayes_predict(X_test, p_ci, p_x_ci)
y_pred == y_test
# === 範例 6 ===
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# === 範例 7 ===
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))
# === 範例 8 ===
model.predict_proba(X_test).round(2)
