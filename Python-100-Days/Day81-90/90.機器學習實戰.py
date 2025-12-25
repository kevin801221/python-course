#!/usr/bin/env python3
"""
從 90.机器学习实战.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import numpy as np
import pandas as pd

df = pd.read_csv('data/train.csv', index_col='PassengerId')
df.head(5)
# === 範例 2 ===
import matplotlib.pyplot as plt

# 修改配置新增中文字型
plt.rcParams['font.sans-serif'].insert(0, 'SimHei')
plt.rcParams['axes.unicode_minus'] = False

# 定製畫布
plt.figure(figsize=(16, 12), dpi=200)

# 遇難和獲救人數分佈
plt.subplot(3, 4, 1)
ser = df.Survived.value_counts()
ser.plot(kind='bar', color=['#BE3144', '#3A7D44'])
plt.xticks(rotation=0)
plt.title('圖1.獲救情況分佈')
plt.ylabel('人數')
plt.xlabel('')
for i, v in enumerate(ser):
    plt.text(i, v, v, ha='center')

# 客艙等級人數分佈
plt.subplot(3, 4, 2)
ser = df.Pclass.value_counts().sort_index()
ser.plot(kind='bar', color=['#FA4032', '#FA812F', '#FAB12F'])
plt.xticks(rotation=0)
plt.ylabel('人數')
plt.xlabel('')
plt.title('圖2.客艙等級分佈')
for i, v in enumerate(ser):
    plt.text(i, v, v, ha='center')

# 性別人數分佈
plt.subplot(3, 4, 3)
ser = df.Sex.value_counts()
ser.plot(kind='bar', color=['#16404D', '#D84040'])
plt.xticks(rotation=0)
plt.ylabel('人數')
plt.xlabel('')
plt.title('圖3.性別分佈')
for i, v in enumerate(ser):
    plt.text(i, v, v, ha='center')

# 登船港口人數分佈
plt.subplot(3, 4, 4)
ser = df.Embarked.value_counts()
ser.plot(kind='bar', color=['#FA4032', '#FA812F', '#FAB12F'])
plt.xticks(rotation=0)
plt.ylabel('人數')
plt.xlabel('')
plt.title('圖4.登船港口分佈')
for i, v in enumerate(ser):
    plt.text(i, v, v, ha='center')

# 乘客年齡箱線圖
plt.subplot(3, 4, 5)
df.Age.plot(kind='box', showmeans=True, notch=True)
plt.title('圖5.乘客年齡情況')

# 船票價格箱線圖
plt.subplot(3, 4, 6)
df.Fare.plot(kind='box', showmeans=True, notch=True)
plt.title('圖6.船票價格情況')

# 不同客艙等級遇難和倖存人數分佈
plt.subplot(3, 4, (7, 8))
s0 = df[df.Survived == 0].Pclass.value_counts()
s1 = df[df.Survived == 1].Pclass.value_counts()
temp = pd.DataFrame({'遇難': s0, '倖存': s1})
pcts = temp.div(temp.sum(axis=1), axis=0)
temp.plot(ax=plt.gca(), kind='bar', stacked=True, color=['#BE3144', '#3A7D44'])
for i, idx in enumerate(temp.index):
    plt.text(i, temp.at[idx, '遇難'] // 2, f'{pcts.at[idx, "遇難"]:.2%}', ha='center', va='center')
    plt.text(i, temp.at[idx, '遇難'] + temp.at[idx, '倖存'] // 2, f'{pcts.at[idx, "倖存"]:.2%}', ha='center', va='center')
plt.xticks(rotation=0)
plt.xlabel('')
plt.title('圖7.不同客艙等級倖存情況')

# 不同性別遇難和倖存人數分佈
plt.subplot(3, 4, (9, 10))
s0 = df[df.Survived == 0].Sex.value_counts()
s1 = df[df.Survived == 1].Sex.value_counts()
temp = pd.DataFrame({'遇難': s0, '倖存': s1})
pcts = temp.div(temp.sum(axis=1), axis=0)
temp.plot(ax=plt.gca(), kind='bar', stacked=True, color=['#BE3144', '#3A7D44'])
for i, idx in enumerate(temp.index):
    plt.text(i, temp.at[idx, '遇難'] // 2, f'{pcts.at[idx, "遇難"]:.2%}', ha='center', va='center')
    plt.text(i, temp.at[idx, '遇難'] + temp.at[idx, '倖存'] // 2, f'{pcts.at[idx, "倖存"]:.2%}', ha='center', va='center')
plt.xticks(rotation=0)
plt.xlabel('')
plt.title('圖8.不同性別倖存情況')

# 不同登船港口遇難和倖存人數分佈
plt.subplot(3, 4, (11, 12))
s0 = df[df.Survived == 0].Embarked.value_counts()
s1 = df[df.Survived == 1].Embarked.value_counts()
temp = pd.DataFrame({'遇難': s0, '倖存': s1})
pcts = temp.div(temp.sum(axis=1), axis=0)
temp.plot(ax=plt.gca(), kind='bar', stacked=True, color=['#BE3144', '#3A7D44'])
for i, idx in enumerate(temp.index):
    plt.text(i, temp.at[idx, '遇難'] // 2, f'{pcts.at[idx, "遇難"]:.2%}', ha='center', va='center')
    plt.text(i, temp.at[idx, '遇難'] + temp.at[idx, '倖存'] // 2, f'{pcts.at[idx, "倖存"]:.2%}', ha='center', va='center')
plt.xticks(rotation=0)
plt.xlabel('')
plt.title('圖9.不同登船港口倖存情況')

plt.show()
# === 範例 3 ===
df.info()
# === 範例 4 ===
df['Age'] = df.Age.fillna(df.Age.median())
df['Embarked'] = df.Embarked.fillna(df.Embarked.mode()[0])
df['Cabin'] = df.Cabin.replace(r'.+', '1', regex=True).replace(np.nan, 0).astype('i8')
# === 範例 5 ===
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[['Fare', 'Age']] = scaler.fit_transform(df[['Fare', 'Age']])
# === 範例 6 ===
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)
# === 範例 7 ===
title_mapping = {
    'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Dr': 4, 'Rev': 5, 'Col': 6, 'Major': 7, 
    'Mlle': 8, 'Ms': 9, 'Lady': 10, 'Sir': 11, 'Jonkheer': 12, 'Don': 13, 'Dona': 14, 'Countess': 15
}
df['Title'] = df['Name'].map(
    lambda x: x.split(',')[1].split('.')[0].strip()
).map(title_mapping).fillna(-1)
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
# === 範例 8 ===
df.drop(columns=['Name', 'SibSp', 'Parch', 'Ticket'], inplace=True)
# === 範例 9 ===
from sklearn.model_selection import train_test_split

X, y = df.drop(columns='Survived'), df.Survived
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.9, random_state=3)
# === 範例 10 ===
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

model = LogisticRegression(penalty='l1', tol=1e-6, solver='liblinear')
model.fit(X_train, y_train)
y_pred = model.predict(X_valid)
print(classification_report(y_valid, y_pred))
# === 範例 11 ===
import xgboost as xgb

# 將資料處理成資料集格式DMatrix格式
dm_train = xgb.DMatrix(X_train, y_train)
dm_valid = xgb.DMatrix(X_valid)

# 設定模型引數
params = {
    'booster': 'gbtree',             # 用於訓練的基學習器型別
    'objective': 'binary:logistic',  # 指定模型的損失函式
    'gamma': 0.1,                    # 控制每次分裂的最小損失函式減少量
    'max_depth': 10,                 # 決策樹最大深度
    'lambda': 0.5,                   # L2正則化權重
    'subsample': 0.8,                # 控制每棵樹訓練時隨機選取的樣本比例
    'colsample_bytree': 0.8,         # 用於控制每棵樹或每個節點的特徵選擇比例
    'eta': 0.05,                     # 學習率
    'seed': 3,                       # 設定隨機數生成器的種子
    'nthread': 16,                   # 指定了訓練時並行使用的執行緒數
}

model = xgb.train(params, dm_train, num_boost_round=200)
y_pred = model.predict(dm_valid)
# 將預測的機率轉換為類別標籤
y_pred_label = (y_pred > 0.5).astype('i8')
print(classification_report(y_valid, y_pred_label))
# === 範例 12 ===
test = pd.read_csv('data/test.csv', index_col='PassengerId')
# 處理缺失值
test['Age'] = test.Age.fillna(test.Age.median())
test['Fare'] = test.Fare.fillna(test.Fare.median())
test['Embarked'] = test.Embarked.fillna(test.Embarked.mode()[0])
test['Cabin'] = test.Cabin.replace(r'.+', '1', regex=True).replace(np.nan, 0).astype('i8')
# 特徵縮放
test[['Fare', 'Age']] = scaler.fit_transform(test[['Fare', 'Age']])
# 處理類別
test = pd.get_dummies(test, columns=['Sex', 'Embarked'], drop_first=True)
# 特徵構造
test['Title'] = test['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip()).map(title_mapping).fillna(-1)
test['FamilySize'] = test['SibSp'] + test['Parch'] + 1
# 刪除多餘特徵
test.drop(columns=['Name', 'Ticket', 'SibSp', 'Parch'], inplace=True)

# 使用邏輯迴歸模型
passenger_id, X_test = test.index, test
# 使用XGBoost模型
# passenger_id, X_test = test.index, xgb.DMatrix(test)

y_test_pred = model.predict(X_test)
# XGoost模型 - 將預測的機率轉換成類別標籤
# y_test_pred = (model.predict(X_test) > 0.5).astype('i8')

# 生成提交檔案
result = pd.DataFrame({
    'PassengerId': passenger_id,
    'Survived': y_test_pred
})
result.to_csv('submission.csv', index=False)
# === 範例 13 ===
import joblib

joblib.dump(model, 'model.pkl')
# === 範例 14 ===
import joblib

model = joblib.load('model.pkl')
model.predict(X_test)
# === 範例 15 ===
from flask import Flask
from flask import jsonify
from flask import request

import joblib
import pandas as pd
import xgboost as xgb

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    query_df = pd.DataFrame(request.json)
    model = joblib.load('model.pkl')
    y_pred = (model.predict(xgb.DMatrix(query_df)) > 0.5).tolist()
    return jsonify({'message': 'OK', 'result': y_pred})


if __name__ == '__main__':
    app.run(debug=True)
