#!/usr/bin/env python3
"""
從 87.集成学习算法.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import classification_report

# 資料集的載入和劃分
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 初始化弱分類器（決策樹樁）
base_estimator = DecisionTreeClassifier(max_depth=1)
# 初始化 AdaBoost 分類器
model = AdaBoostClassifier(base_estimator, n_estimators=50)
# 訓練模型
model.fit(X_train, y_train)
# 預測結果
y_pred = model.predict(X_test)

# 輸出評估報告
print(classification_report(y_test, y_pred))
# === 範例 2 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report

# 資料集的載入和劃分
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 初始化 GBDT 分類器
model = GradientBoostingClassifier(n_estimators=32)
# 訓練模型
model.fit(X_train, y_train)
# 預測結果
y_pred = model.predict(X_test)

# 輸出評估報告
print(classification_report(y_test, y_pred))
# === 範例 3 ===
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 資料集的載入和劃分
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 將資料處理成資料集格式DMatrix格式
dm_train = xgb.DMatrix(X_train, y_train)
dm_test = xgb.DMatrix(X_test)

# 設定模型引數
params = {
    'booster': 'gbtree',           # 用於訓練的基學習器型別
    'objective': 'multi:softmax',  # 指定模型的損失函式
    'num_class': 3,                # 類別的數量
    'gamma': 0.1,                  # 控制每次分裂的最小損失函式減少量
    'max_depth': 6,                # 決策樹最大深度
    'lambda': 2,                   # L2正則化權重
    'subsample': 0.8,              # 控制每棵樹訓練時隨機選取的樣本比例
    'colsample_bytree': 0.8,       # 用於控制每棵樹或每個節點的特徵選擇比例
    'eta': 0.001,                  # 學習率
    'seed': 10,                    # 設定隨機數生成器的種子
    'nthread': 16,                 # 指定了訓練時並行使用的執行緒數
}

# 訓練模型
model = xgb.train(params, dm_train, num_boost_round=200)
# 預測結果
y_pred = model.predict(dm_test)

# 輸出模型評估報告
print(classification_report(y_test, y_pred))

# 繪製特徵重要性評分
xgb.plot_importance(model)
plt.grid(False)
plt.show()
# === 範例 4 ===
import lightgbm as lgb
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 載入和劃分資料集
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 將資料轉化為 LightGBM 的資料格式
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# 設定模型引數
params = {
    'objective': 'multiclass',   # 多分類問題
    'num_class': 3,              # 類別數量
    'metric': 'multi_logloss',   # 多分類對數損失函式
    'boosting_type': 'gbdt',     # 使用梯度提升樹演算法
    'num_leaves': 31,            # 葉子節點數
    'learning_rate': 0.05,       # 學習率
    'feature_fraction': 0.75,    # 每次訓練時隨機選擇特徵的比例
    'early_stopping_rounds': 10  # 連續多少論沒有效能提升就停止迭代
}
# 模型訓練
model = lgb.train(params=params, train_set=train_data, num_boost_round=200, valid_sets=[test_data])
# 模型預測
y_pred = model.predict(X_test, num_iteration=model.best_iteration)
# 將預測結果處理成標籤
y_pred_max = np.argmax(y_pred, axis=1)

# 檢視模型評估報告
print(classification_report(y_test, y_pred_max))
