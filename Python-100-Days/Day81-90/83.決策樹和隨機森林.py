#!/usr/bin/env python3
"""
從 83.决策树和随机森林.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import numpy as np


def entropy(y):
    """
    計算資訊熵
    :param y: 資料集的目標值
    :return: 資訊熵
    """
    _, counts = np.unique(y, return_counts=True)
    prob = counts / y.size
    return -np.sum(prob * np.log2(prob))


def info_gain(x, y):
    """
    計算資訊增益
    :param x: 給定的特徵
    :param y: 資料集的目標值
    :return: 資訊增益
    """
    values, counts = np.unique(x, return_counts=True)
    new_entropy = 0
    for i, value in enumerate(values):
        prob = counts[i] / x.size
        new_entropy += prob * entropy(y[x == value])
    return entropy(y) - new_entropy
# === 範例 2 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)
print(f'H(D)    = {entropy(y_train)}')
print(f'g(D,A0) = {info_gain(X_train[:, 0], y_train)}')
print(f'g(D,A1) = {info_gain(X_train[:, 1], y_train)}')
print(f'g(D,A2) = {info_gain(X_train[:, 2], y_train)}')
print(f'g(D,A3) = {info_gain(X_train[:, 3], y_train)}')
# === 範例 3 ===
def info_gain_ratio(x, y):
    """
    計算資訊增益比
    :param x: 給定的特徵
    :param y: 資料集的目標值
    :return: 資訊增益比
    """
    return info_gain(x, y) / entropy(x)


print(f'R(D,A0) = {info_gain_ratio(X_train[:, 0], y_train)}')
print(f'R(D,A1) = {info_gain_ratio(X_train[:, 1], y_train)}')
print(f'R(D,A2) = {info_gain_ratio(X_train[:, 2], y_train)}')
print(f'R(D,A3) = {info_gain_ratio(X_train[:, 3], y_train)}')
# === 範例 4 ===
def gini_index(y):
    """
    計算基尼指數
    :param y: 資料集的目標值
    :return: 基尼指數
    """
    _, counts = np.unique(y, return_counts=True)
    return 1 - np.sum((counts / y.size) ** 2)


def gini_with_feature(x, y):
    """
    計算給定特徵後的基尼指數
    :param x: 給定的特徵
    :param y: 資料集的目標值
    :return: 給定特徵後的基尼指數
    """
    values, counts = np.unique(x, return_counts=True)
    gini = 0
    for value in values:
        prob = x[x == value].size / x.size
        gini += prob * gini_index(y[x == value]) 
    return gini


print(f'G(D)    = {gini_index(y_train)}')
print(f'G(D,A0) = {gini_with_feature(X_train[:, 0], y_train)}')
print(f'G(D,A1) = {gini_with_feature(X_train[:, 1], y_train)}')
print(f'G(D,A2) = {gini_with_feature(X_train[:, 2], y_train)}')
print(f'G(D,A3) = {gini_with_feature(X_train[:, 3], y_train)}')
# === 範例 5 ===
from sklearn.tree import DecisionTreeClassifier

# 建立模型
model = DecisionTreeClassifier()
# 訓練模型
model.fit(X_train, y_train)
# 預測結果
y_pred = model.predict(X_test)
# === 範例 6 ===
from sklearn.metrics import classification_report

print(y_test)
print(y_pred)
print(classification_report(y_test, y_pred))
# === 範例 7 ===
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(12, 10))
plot_tree(
    decision_tree=model,               # 決策樹模型
    feature_names=iris.feature_names,  # 特徵的名稱
    class_names=iris.target_names,     # 標籤的名稱
    filled=True                        # 用顏色填充
)
plt.show()
# === 範例 8 ===
# 建立模型
model = DecisionTreeClassifier(
    criterion='entropy',
    ccp_alpha=0.01,
    
)
# 訓練模型
model.fit(X_train, y_train)
# 視覺化
plt.figure(figsize=(12, 10))
plot_tree(
    decision_tree=model,               # 決策樹模型
    feature_names=iris.feature_names,  # 特徵的名稱
    class_names=iris.target_names,     # 標籤的名稱
    filled=True                        # 用顏色填充
)
plt.show()
# === 範例 9 ===
from sklearn.model_selection import GridSearchCV

gs = GridSearchCV(
    estimator=DecisionTreeClassifier(),
    param_grid={
        'criterion': ['gini', 'entropy'],
        'max_depth': np.arange(5, 10),
        'max_features': [None, 'sqrt', 'log2'],
        'min_samples_leaf': np.arange(1, 11),
        'max_leaf_nodes': np.arange(5, 15)
    },
    cv=5
)
gs.fit(X_train, y_train)
# === 範例 10 ===
from sklearn.ensemble import RandomForestClassifier

gs = GridSearchCV(
    estimator=RandomForestClassifier(n_jobs=-1),
    param_grid={
        'n_estimators': [50, 100, 150],
        'criterion': ['gini', 'entropy'],
        'max_depth': np.arange(5, 10),
        'max_features': ['sqrt', 'log2'],
        'min_samples_leaf': np.arange(1, 11),
        'max_leaf_nodes': np.arange(5, 15)
    },
    cv=5
)
gs.fit(X_train, y_train)
