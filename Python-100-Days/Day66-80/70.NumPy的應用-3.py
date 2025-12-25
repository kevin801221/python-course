#!/usr/bin/env python3
"""
從 70.NumPy的应用-3.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
array1 = np.arange(1, 10)
print(array1 + 10)
print(array1 * 10)
# === 範例 2 ===
print(array1 > 5)
print(array1 % 2 == 0)
# === 範例 3 ===
array2 = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3])
print(array1 + array2)
print(array1 * array2)
print(array1 ** array2)
# === 範例 4 ===
print(array1 > array2)
print(array1 % array2 == 0)
# === 範例 5 ===
print(np.sqrt(array1))
print(np.log2(array1))
# === 範例 6 ===
array3 = np.array([[4, 5, 6], [7, 8, 9]])
array4 = np.array([[1, 2, 3], [3, 2, 1]])
print(np.maximum(array3, array4))
print(np.power(array3, array4))
# === 範例 7 ===
array5 = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3]])
array6 = np.array([1, 2, 3])
array5 + array6
# === 範例 8 ===
array7 = np.array([[1], [2], [3], [4]])
array5 + array7
# === 範例 9 ===
np.unique(array5)
# === 範例 10 ===
array8 = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
array9 = np.array([[4, 4, 4], [5, 5, 5], [6, 6, 6]])
np.hstack((array8, array9))
# === 範例 11 ===
np.vstack((array8, array9))
# === 範例 12 ===
np.concatenate((array8, array9))
# === 範例 13 ===
np.concatenate((array8, array9), axis=1)
# === 範例 14 ===
np.append(array1, [10, 100])
# === 範例 15 ===
np.insert(array1, 1, [98, 99, 100])
# === 範例 16 ===
np.extract(array1 % 2 != 0, array1)
# === 範例 17 ===
np.select([array1 <= 3, array1 >= 7], [array1 * 10, array1 ** 2])
# === 範例 18 ===
np.where(array1 <= 5, array1 * 10, array1 ** 2)
# === 範例 19 ===
np.repeat(array1, 3)
# === 範例 20 ===
np.tile(array1, 2)
# === 範例 21 ===
np.resize(array1, (5, 3))
# === 範例 22 ===
np.resize(array5, (2, 4))
# === 範例 23 ===
np.put(array1, [0, 1, -1, 3, 5], [100, 200])
array1
# === 範例 24 ===
np.place(array1, array1 > 5, [1, 2, 3])
array1
