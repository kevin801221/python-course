#!/usr/bin/env python3
"""
從 78.数据可视化-1.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
plt.figure(figsize=(6, 4), dpi=120)
# 繪製直方圖
plt.hist(heights, bins=np.arange(145, 196, 5), color='darkcyan', density=True, cumulative=True)
# 定製橫軸標籤
plt.xlabel('身高')
# 定製縱軸標籤
plt.ylabel('機率')
plt.show()
