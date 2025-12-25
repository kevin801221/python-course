#!/usr/bin/env python3
"""
從 82.k最近邻算法.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
# 特徵（150行4列的二維陣列，分別是花萼長、花萼寬、花瓣長、花瓣寬）
X = iris.data
# 標籤（150個元素的一維陣列，包含0、1、2三個值分別代表三種鳶尾花）
y = iris.target
# === 範例 2 ===
# 將特徵和標籤堆疊到同一個陣列中
data = np.hstack((X, y.reshape(-1, 1)))
# 透過隨機亂序函式將原始資料打亂
np.random.shuffle(data)
# 選擇80%的資料作為訓練集
train_size = int(y.size * 0.8)
train, test = data[:train_size], data[train_size:]
X_train, y_train = train[:, :-1], train[:, -1]
X_test, y_test = test[:, :-1], test[:, -1]
# === 範例 3 ===
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)
# === 範例 4 ===
import numpy as np


def euclidean_distance(u, v):
    """計算兩個n維向量的歐式距離"""
    return np.sqrt(np.sum(np.abs(u - v) ** 2))
# === 範例 5 ===
from scipy import stats


def make_label(X_train, y_train, X_one, k):
    """
    根據歷史資料中k個最近鄰為新資料生成標籤
    :param X_train: 訓練集中的特徵
    :param y_train: 訓練集中的標籤
    :param X_one: 待預測的樣本（新資料）特徵
    :param k: 鄰居的數量
    :return: 為待預測樣本生成的標籤（鄰居標籤的眾數）
    """
    # 計算x跟每個訓練樣本的距離
    distes = [euclidean_distance(X_one, X_i) for X_i in X_train]
    # 透過一次劃分找到k個最小距離對應的索引並獲取到相應的標籤
    labels = y_train[np.argpartition(distes, k - 1)[:k]]
    # 獲取標籤的眾數
    return stats.mode(labels).mode
# === 範例 6 ===
def predict_by_knn(X_train, y_train, X_new, k=5):
    """
    KNN演算法
    :param X_train: 訓練集中的特徵
    :param y_train: 訓練集中的標籤
    :param X_new: 待預測的樣本構成的陣列
    :param k: 鄰居的數量（預設值為5）
    :return: 儲存預測結果（標籤）的陣列
    """
    return np.array([make_label(X_train, y_train, X, k) for X in X_new])
# === 範例 7 ===
y_pred = predict_by_knn(X_train, y_train, X_test)
y_pred == y_test
# === 範例 8 ===
from sklearn.neighbors import KNeighborsClassifier

# 建立模型
model = KNeighborsClassifier()
# 訓練模型
model.fit(X_train, y_train)
# 預測結果
y_pred = model.predict(X_test)
# === 範例 9 ===
y_pred == y_test
# === 範例 10 ===
model.score(X_test, y_test)
# === 範例 11 ===
print(y_test)
print(y_pred)
# === 範例 12 ===
from sklearn.metrics import classification_report, confusion_matrix

# 輸出分類模型混淆矩陣
print('混淆矩陣: ')
print(confusion_matrix(y_test, y_pred))
# 輸出分類模型評估報告
print('評估報告: ')
print(classification_report(y_test, y_pred))
# === 範例 13 ===
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

# 建立混淆矩陣顯示物件
cm_display_obj = ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred), display_labels=iris.target_names)
# 繪製並顯示混淆矩陣
cm_display_obj.plot(cmap=plt.cm.Reds)
plt.show()
# === 範例 14 ===
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import RocCurveDisplay

# 手動構造一組真實值和對應的預測值
y_test_ex = np.array([0, 0, 0, 1, 1, 0, 1, 1, 1, 0])
y_pred_ex = np.array([1, 0, 0, 1, 1, 0, 1, 1, 0, 1])
# 透過roc_curve函式計算出FPR（假正例率）和TPR（真正例率）
fpr, tpr, _ = roc_curve(y_test_ex, y_pred_ex)
# 透過auc函式計算出AUC值並透過RocCurveDisplay類繪製圖形
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc(fpr, tpr)).plot()
plt.show()
# === 範例 15 ===
from sklearn.model_selection import GridSearchCV

# 網格搜尋交叉驗證
gs = GridSearchCV(
    estimator=KNeighborsClassifier(),
    param_grid={
        'n_neighbors': [1, 3, 5, 7, 9, 11, 13, 15],
        'weights': ['uniform', 'distance'],
        'p': [1, 2]
    },
    cv=5
)
gs.fit(X_train, y_train)
# === 範例 16 ===
print('最優引數:', gs.best_params_)
print('評分:', gs.best_score_)
# === 範例 17 ===
gs.predict(X_test)
# === 範例 18 ===
# 每月收入
incomes = np.array([
    9558, 8835, 9313, 14990, 5564, 11227, 11806, 10242, 11999, 11630,
    6906, 13850, 7483, 8090, 9465, 9938, 11414, 3200, 10731, 19880,
    15500, 10343, 11100, 10020, 7587, 6120, 5386, 12038, 13360, 10885,
    17010, 9247, 13050, 6691, 7890, 9070, 16899, 8975, 8650, 9100,
    10990, 9184, 4811, 14890, 11313, 12547, 8300, 12400, 9853, 12890
])
# 每月網購支出
outcomes = np.array([
    3171, 2183, 3091, 5928, 182, 4373, 5297, 3788, 5282, 4166,
    1674, 5045, 1617, 1707, 3096, 3407, 4674, 361, 3599, 6584,
    6356, 3859, 4519, 3352, 1634, 1032, 1106, 4951, 5309, 3800,
    5672, 2901, 5439, 1478, 1424, 2777, 5682, 2554, 2117, 2845,
    3867, 2962,  882, 5435, 4174, 4948, 2376, 4987, 3329, 5002
])
X = np.sort(incomes).reshape(-1, 1)  # 將收入排序後處理成二維陣列
y = outcomes[np.argsort(incomes)]    # 將網購支出按照收入進行排序
# === 範例 19 ===
from sklearn.neighbors import KNeighborsRegressor

# 建立模型
model = KNeighborsRegressor()
# 訓練模型
model.fit(X, y)
# 預測結果
y_pred = model.predict(X)
# === 範例 20 ===
# 原始資料散點圖
plt.scatter(X, y, color='navy')
# 預測結果折線圖
plt.plot(X, y_pred, color='coral')
plt.show()
