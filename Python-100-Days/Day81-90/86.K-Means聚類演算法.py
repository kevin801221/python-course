#!/usr/bin/env python3
"""
從 86.K-Means聚类算法.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import numpy as np


def distance(u, v, p=2):
    """計算兩個向量的距離"""
    return np.sum(np.abs(u - v) ** p) ** (1 / p)


def init_centroids(X, k):
    """隨機選擇k個質心"""
    index = np.random.choice(np.arange(len(X)), k, replace=False)
    return X[index]


def closest_centroid(sample, centroids):
    """找到跟樣本最近的質心"""
    distances = [distance(sample, centroid) for i, centroid in enumerate(centroids)]
    return np.argmin(distances)


def build_clusters(X, centroids):
    """根據質心將資料分成簇"""
    clusters = [[] for _ in range(len(centroids))]
    for i, sample in enumerate(X):
        centroid_index = closest_centroid(sample, centroids)
        clusters[centroid_index].append(i)
    return clusters


def update_centroids(X, clusters):
    """更新質心的位置"""
    return np.array([np.mean(X[cluster], axis=0) for cluster in clusters])


def make_label(X, clusters):
    """生成標籤"""
    labels = np.zeros(len(X))
    for i, cluster in enumerate(clusters):
        for j in cluster:
            labels[j] = i
    return labels


def kmeans(X, *, k, max_iter=1000, tol=1e-4):
    """KMeans聚類"""
    # 隨機選擇k個質心
    centroids = init_centroids(X, k)
    # 透過不斷的迭代對資料進行劃分
    for _ in range(max_iter):
        # 透過質心將資料劃分到不同的簇
        clusters = build_clusters(X, centroids)
        # 重新計算新的質心的位置
        new_centroids = update_centroids(X, clusters)
        # 如果質心幾乎沒有變化就提前終止迭代
        if np.allclose(new_centroids, centroids, rtol=tol):
            break
        # 記錄新的質心的位置
        centroids = new_centroids
    # 給資料生成標籤
    return make_label(X, clusters), centroids
# === 範例 2 ===
from sklearn.datasets import load_iris

iris = load_iris()
X, y = iris.data, iris.target
labels, centers = kmeans(X, k=3)
# === 範例 3 ===
import matplotlib.pyplot as plt

colors = ['#FF6969', '#050C9C', '#365E32']
markers = ['o', 'x', '^']

plt.figure(dpi=200)
for i in range(len(centers)):
    samples = X[labels == i]
    print(markers[i])
    plt.scatter(samples[:, 2], samples[:, 3], marker=markers[i], color=colors[i])
    plt.scatter(centers[i, 2], centers[i, 3], marker='*', color='r', s=120)

plt.xlabel('Petal length')
plt.ylabel('Petal width')
plt.show()
# === 範例 4 ===
import matplotlib.pyplot as plt

colors = ['#FF6969', '#050C9C', '#365E32']
markers = ['o', 'x', '^']

plt.figure(dpi=200)
for i in range(len(centers)):
    samples = X[y == i]
    plt.scatter(samples[:, 2], samples[:, 3], marker=markers[i], color=colors[i])

plt.xlabel('Petal length')
plt.ylabel('Petal width')
plt.show()
# === 範例 5 ===
from sklearn.cluster import KMeans

# 建立KMeans物件
km_cluster = KMeans(
    n_clusters=3,       # k值（簇的數量）
    max_iter=30,        # 最大迭代次數
    n_init=10,          # 初始質心選擇嘗試次數
    init='k-means++',   # 初始質心選擇演算法
    algorithm='elkan',  # 是否使用三角不等式最佳化
    tol=1e-4,           # 質心變化容忍度
    random_state=3      # 隨機數種子
)
# 訓練模型
km_cluster.fit(X)
print(km_cluster.labels_)           # 分簇的標籤
print(km_cluster.cluster_centers_)  # 各個質心的位置
print(km_cluster.inertia_)          # 樣本到質心的距離平方和
