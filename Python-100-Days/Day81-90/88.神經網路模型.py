#!/usr/bin/env python3
"""
從 88.神经网络模型.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

# 載入和劃分資料集
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 建立多層感知機分類器模型
model = MLPClassifier(
    solver='lbfgs',            # 最佳化模型引數的求解器
    learning_rate='adaptive',  # 學習率的調節方式為自適應 
    activation='relu',         # 隱藏層中神經元的啟用函式 
    hidden_layer_sizes=(1, )   # 每一層神經元的數量
)
# 訓練和預測
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 檢視模型評估報告
print(classification_report(y_test, y_pred))
# === 範例 2 ===
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

# 載入和劃分資料集
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)

# 建立多層感知機分類器模型
model = MLPClassifier(
    solver='lbfgs',                  # 最佳化模型引數的求解器
    learning_rate='adaptive',        # 學習率的調節方式為自適應 
    activation='relu',               # 隱藏層中神經元的啟用函式 
    hidden_layer_sizes=(32, 32, 32)  # 每一層神經元的數量
)
# 訓練和預測
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 檢視模型評估報告
print(classification_report(y_test, y_pred))
# === 範例 3 ===
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# 載入鳶尾花資料集
iris = datasets.load_iris()
X, y = iris.data, iris.target

# 資料預處理（標準化）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 劃分訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, train_size=0.8, random_state=3)
# 將陣列轉換為PyTorch張量
X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = (
    torch.tensor(X_train, dtype=torch.float32),
    torch.tensor(X_test, dtype=torch.float32),
    torch.tensor(y_train, dtype=torch.long),
    torch.tensor(y_test, dtype=torch.long)
)


class IrisNN(nn.Module):
    """鳶尾花神經網路模型"""

    def __init__(self):
        """初始化方法"""
        # 呼叫父類構造器
        super(IrisNN, self).__init__()
        # 輸入層到隱藏層（4個特徵到32個神經元全連線）
        self.fc1 = nn.Linear(4, 32)
        # 隱藏層到輸出層（32個神經元到3個輸出全連線）
        self.fc2 = nn.Linear(32, 3)

    def forward(self, x):
        """前向傳播"""
        # 隱藏層使用ReLU啟用函式
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 建立模型例項
model = IrisNN()
# 定義損失函式（交叉熵損失函式）
loss_function = nn.CrossEntropyLoss()
# 使用Adam最佳化器（大多數任務表現較好）
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 訓練模型（迭代256個輪次）
for _ in range(256):
    model.train()
    # 清除上一次的梯度
    optimizer.zero_grad()
    # 計算輸出
    output = model(X_train_tensor)
    # 計算損失
    loss = loss_function(output, y_train_tensor)
    # 反向傳播
    loss.backward()
    # 更新權重
    optimizer.step()

# 評估模型
model.eval()
with torch.no_grad():
    output = model(X_test_tensor)
    # 獲取預測得分最大值的索引（預測標籤）
    _, y_pred_tensor = torch.max(output, 1)
    # 計算並輸出預測準確率
    print(f'Accuracy: {accuracy_score(y_test_tensor, y_pred_tensor):.2%}')
    # 輸出分類模型評估報告
    print(classification_report(y_test_tensor, y_pred_tensor))
# === 範例 4 ===
import ssl

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ssl._create_default_https_context = ssl._create_unverified_context


def load_prep_data():
    """載入準備資料"""
    df = pd.read_csv('https://archive.ics.uci.edu/static/public/9/data.csv')
    # 對特徵進行清洗
    df.drop(columns=['car_name'], inplace=True)
    df.dropna(inplace=True)
    df['origin'] = df['origin'].astype('category')
    df = pd.get_dummies(df, columns=['origin'], drop_first=True).astype('f8')
    # 對特徵進行縮放
    scaler = StandardScaler()
    return scaler.fit_transform(df.drop(columns='mpg').values), df['mpg'].values


class MLPRegressor(nn.Module):
    """神經網路模型"""

    def __init__(self, n):
        super(MLPRegressor, self).__init__()
        self.fc1 = nn.Linear(n, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def main():
    # 載入和準備資料集
    X, y = load_prep_data()
    # 劃分訓練集和測試集
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=3)
    # 將資料轉為PyTorch的Tensor
    X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = (
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(X_test, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32).view(-1, 1),
        torch.tensor(y_test, dtype=torch.float32).view(-1, 1)
    )

    # 例項化神經網路模型
    model = MLPRegressor(X_train.shape[1])
    # 指定損失函式（均方誤差）
    criterion = nn.MSELoss()
    # 指定最佳化器（Adam最佳化器）
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 模型訓練
    epochs = 256
    for epoch in range(epochs):
        # 前向傳播
        y_pred_tensor = model(X_train_tensor)
        loss = criterion(y_pred_tensor, y_train_tensor)
        # 反向傳播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 16 == 0:
            print(f'Epoch [{epoch + 1} / {epochs}], Loss: {loss.item():.4f}')

    # 模型評估
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test_tensor)
        test_loss = mean_squared_error(y_test, y_pred.numpy())
        r2 = r2_score(y_test, y_pred.numpy())
    print(f'Test MSE: {test_loss:.4f}')
    print(f'Test R2: {r2:.4f}')


if __name__ == '__main__':
    main()
