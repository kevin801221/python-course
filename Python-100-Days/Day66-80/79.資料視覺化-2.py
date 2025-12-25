#!/usr/bin/env python3
"""
從 79.数据可视化-2.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
income = np.array([5550, 7500, 10500, 15000, 20000, 25000, 30000, 40000])
outcome = np.array([800, 1800, 1250, 2000, 1800, 2100, 2500, 3500])
nums = np.array([5, 3, 10, 5, 12, 20, 8, 10])

# 透過scatter函式的s引數和c引數分別控制面積和顏色
plt.scatter(income, outcome, s=nums * 30, c=nums, cmap='Reds')
# 顯示顏色條
plt.colorbar()
# 顯示圖表
plt.show()
# === 範例 2 ===
plt.figure(figsize=(8, 4))
days = np.arange(7)
sleeping = [7, 8, 6, 6, 7, 8, 10]
eating = [2, 3, 2, 1, 2, 3, 2]
working = [7, 8, 7, 8, 6, 2, 3]
playing = [8, 5, 9, 9, 9, 11, 9]
# 繪製堆疊折線圖
plt.stackplot(days, sleeping, eating, working, playing)
# 定製橫軸刻度
plt.xticks(days, labels=[f'星期{x}' for x in '一二三四五六日'])
# 定製圖例
plt.legend(['睡覺', '吃飯', '工作', '玩耍'], fontsize=10)
# 顯示圖表
plt.show()
# === 範例 3 ===
labels = np.array(['速度', '力量', '經驗', '防守', '發球', '技術'])
# 馬龍和水谷隼的資料
malong_values = np.array([93, 95, 98, 92, 96, 97])
shuigu_values = np.array([30, 40, 65, 80, 45, 60])
angles = np.linspace(0, 2 * np.pi, labels.size, endpoint=False)
# 多加一條資料讓圖形閉合
malong_values = np.append(malong_values, malong_values[0])
shuigu_values = np.append(shuigu_values, shuigu_values[0])
angles = np.append(angles, angles[0])
# 建立畫布
plt.figure(figsize=(4, 4), dpi=120)
# 建立座標系
ax = plt.subplot(projection='polar')
# 繪圖和填充
plt.plot(angles, malong_values, color='r', linewidth=2, label='馬龍')
plt.fill(angles, malong_values, color='r', alpha=0.3)
plt.plot(angles, shuigu_values, color='g', linewidth=2, label='水谷隼')
plt.fill(angles, shuigu_values, color='g', alpha=0.2)
# 顯示圖例
ax.legend()
# 顯示圖表
plt.show()
# === 範例 4 ===
group1 = np.random.randint(20, 50, 4)
group2 = np.random.randint(10, 60, 4)
x = np.array([f'A組-Q{i}' for i in range(1, 5)] + [f'B組-Q{i}' for i in range(1, 5)])
y = np.array(group1.tolist() + group2.tolist())
# 玫瑰花瓣的角度和寬度
theta = np.linspace(0, 2 * np.pi, x.size, endpoint=False)
width = 2 * np.pi / x.size
# 生成8種隨機顏色
colors = np.random.rand(8, 3)
# 將柱狀圖投影到極座標
ax = plt.subplot(projection='polar')
# 繪製柱狀圖
plt.bar(theta, y, width=width, color=colors, bottom=0)
# 設定網格
ax.set_thetagrids(theta * 180 / np.pi, x, fontsize=10)
# 顯示圖表
plt.show()
# === 範例 5 ===
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(8, 4), dpi=120)
# 建立3D座標系並新增到畫布上
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)
x = np.arange(-2, 2, 0.1)
y = np.arange(-2, 2, 0.1)
x, y = np.meshgrid(x, y)
z = (1 - y ** 5 + x ** 5) * np.exp(-x ** 2 - y ** 2)
# 繪製3D曲面
ax.plot_surface(x, y, z)
# 顯示圖表
plt.show()
