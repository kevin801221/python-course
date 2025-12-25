#!/usr/bin/env python3
"""
從 89.自然语言处理入门.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from sklearn.feature_extraction.text import CountVectorizer

# 文件列表
documents = [
    'I love programming.',
    'I love machine learning.',
    'I love apple.'
]

# 建立詞袋模型
cv = CountVectorizer()
X = cv.fit_transform(documents)

# 輸出詞彙表和詞頻向量
print('詞彙表:\n', cv.get_feature_names_out())
print('詞頻向量:\n', X.toarray())
# === 範例 2 ===
import jieba
from sklearn.feature_extraction.text import CountVectorizer

# 文件列表
documents = [
    '我在四川大學讀書',
    '四川大學是四川最好的大學',
    '大學校園裡面有很多學生',
]

# 建立詞袋模型並指定分詞函式
cv = CountVectorizer(
    tokenizer=lambda x: jieba.cut(x),
    token_pattern=None
)
X = cv.fit_transform(documents)

# 輸出詞彙表和詞頻向量
print('詞彙表:\n', cv.get_feature_names_out())
print('詞頻向量:\n', X.toarray())
# === 範例 3 ===
import jieba
from sklearn.feature_extraction.text import CountVectorizer

with open('哈工大停用詞表.txt') as file_obj:
    stop_words_list = file_obj.read().split('\n')

# 文件列表
documents = [
    '我在四川大學讀書',
    '四川大學是四川最好的大學',
    '大學校園裡面有很多學生',
]

# 建立詞袋模型並指定分詞函式
cv = CountVectorizer(
    tokenizer=lambda x: jieba.lcut(x),
    token_pattern=None,
    stop_words=stop_words_list
)
X = cv.fit_transform(documents)

# 輸出詞彙表和詞頻向量
print('詞彙表:\n', cv.get_feature_names_out())
print('詞頻向量:\n', X.toarray())
# === 範例 4 ===
import re

from datasets import load_dataset
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# 載入 IMDB 資料集
imdb = load_dataset('imdb')
# 直接將 50000 條評論用作語料
temp = [imdb['unsupervised'][i]['text'] for i in range(50000)]
# 用正規表示式對評論文字進行簡單處理
corpus = [re.sub(r'[^\w\s]', '', x) for x in temp]

# 預處理語料庫（英文分詞）
sentences = [sentence.lower().split() for sentence in corpus]
# 訓練 Word2Vec 模型
# sentences - 輸入語料庫（句子構成的列表，每個句子是一個或多個單詞的列表）
# vector_size - 詞向量的維度（維度越高能夠表示的資訊越多）
# windows - 上下文視窗大小（模型在訓練時使用的上下文單詞的範圍）
# min_count - 忽略頻率低於此值的單詞（過濾掉在語料庫中出現次數較少的單詞）
# workers - 訓練時使用的 CPU 核心數量
# seed - 隨機數種子（用於初始化模型的權重）
model = Word2Vec(sentences, vector_size=100, window=10, min_count=2, workers=4, seed=3)

# 透過模型獲取 king 和 queen 的詞向量
king_vec, queen_vec = model.wv['king'], model.wv['queen']

# 計算兩個詞向量的餘弦相似度
cos_similarity = cosine_similarity([king_vec], [queen_vec])
print(f'king 和 queen 的餘弦相似度: {cos_similarity[0, 0]:.2f}')

# 透過詞向量進行推理（king - man + woman ≈ queen）
man_vec, woman_vec = model.wv['man'], model.wv['woman']
result_vec = king_vec - man_vec + woman_vec
# 查詢與計算結果最相似的三個詞
similar_words = model.wv.similar_by_vector(result_vec, topn=3)
print(f'跟 king - man + woman 最相似的詞:\n {similar_words}')

# 查詢與 dog 最相似的五個詞
dog_similar_words = model.wv.most_similar('dog', topn=5)
print(f'跟 dog 最相似的詞:\n {dog_similar_words}')
