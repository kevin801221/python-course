"""
標籤管理系統 - Tag Management System
====================================
進階應用：展示 Python 集合的特性與應用

功能：
1. 集合的基本操作
2. 交集、聯集、差集運算
3. 標籤系統實作
4. 相似度計算
"""


class Article:
    """文章類別"""

    def __init__(self, title: str, tags: set = None):
        self.title = title
        self.tags = tags or set()

    def add_tag(self, tag: str):
        """新增標籤"""
        self.tags.add(tag.lower())

    def remove_tag(self, tag: str):
        """移除標籤"""
        self.tags.discard(tag.lower())

    def has_tag(self, tag: str) -> bool:
        """檢查是否有標籤"""
        return tag.lower() in self.tags


class TagManager:
    """標籤管理器"""

    def __init__(self):
        self.articles = []
        self.all_tags = set()  # 所有使用過的標籤

    def add_article(self, title: str, tags: list = None):
        """新增文章"""
        tag_set = set(t.lower() for t in (tags or []))
        article = Article(title, tag_set)
        self.articles.append(article)
        self.all_tags.update(tag_set)  # 集合聯集
        return article

    def get_all_tags(self) -> set:
        """取得所有標籤"""
        return self.all_tags.copy()

    def get_articles_by_tag(self, tag: str) -> list:
        """依標籤搜尋文章"""
        tag = tag.lower()
        return [a for a in self.articles if tag in a.tags]

    def get_articles_by_any_tags(self, tags: list) -> list:
        """任一標籤符合（聯集）"""
        tag_set = set(t.lower() for t in tags)
        return [a for a in self.articles if a.tags & tag_set]  # 交集不為空

    def get_articles_by_all_tags(self, tags: list) -> list:
        """所有標籤都符合（交集）"""
        tag_set = set(t.lower() for t in tags)
        return [a for a in self.articles if tag_set <= a.tags]  # 子集

    def get_common_tags(self, article1: Article, article2: Article) -> set:
        """取得共同標籤（交集）"""
        return article1.tags & article2.tags

    def get_unique_tags(self, article1: Article, article2: Article) -> tuple:
        """取得獨特標籤（差集）"""
        only_in_1 = article1.tags - article2.tags
        only_in_2 = article2.tags - article1.tags
        return only_in_1, only_in_2

    def get_all_different_tags(self, article1: Article, article2: Article) -> set:
        """取得所有不同標籤（對稱差集）"""
        return article1.tags ^ article2.tags

    def calculate_similarity(self, article1: Article, article2: Article) -> float:
        """計算相似度（Jaccard 係數）"""
        if not article1.tags and not article2.tags:
            return 0.0
        intersection = len(article1.tags & article2.tags)
        union = len(article1.tags | article2.tags)
        return intersection / union if union > 0 else 0.0

    def find_similar_articles(self, article: Article, threshold: float = 0.3) -> list:
        """找出相似文章"""
        similar = []
        for other in self.articles:
            if other != article:
                similarity = self.calculate_similarity(article, other)
                if similarity >= threshold:
                    similar.append((other, similarity))
        return sorted(similar, key=lambda x: x[1], reverse=True)

    def get_tag_statistics(self) -> dict:
        """標籤統計"""
        stats = {}
        for article in self.articles:
            for tag in article.tags:
                stats[tag] = stats.get(tag, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

    def add_sample_data(self):
        """新增範例資料"""
        samples = [
            ("Python 基礎教學", ["python", "programming", "beginner"]),
            ("Python 進階技巧", ["python", "programming", "advanced"]),
            ("JavaScript 入門", ["javascript", "programming", "beginner", "web"]),
            ("React 元件開發", ["javascript", "react", "web", "frontend"]),
            ("Django 網站開發", ["python", "django", "web", "backend"]),
            ("資料庫設計", ["database", "sql", "backend"]),
            ("機器學習入門", ["python", "machine-learning", "ai"]),
            ("深度學習實戰", ["python", "deep-learning", "ai", "advanced"]),
        ]
        for title, tags in samples:
            self.add_article(title, tags)


def display_articles(articles, title="文章列表"):
    """顯示文章列表"""
    print(f"\n{'='*60}")
    print(f"  {title} ({len(articles)} 篇)")
    print('='*60)

    for i, article in enumerate(articles, 1):
        tags_str = ', '.join(f"#{t}" for t in sorted(article.tags))
        print(f"  {i}. {article.title}")
        print(f"     標籤: {tags_str}")
    print('='*60)


def demonstrate_set_operations():
    """展示集合運算"""
    print("\n" + "="*60)
    print("  集合運算展示")
    print("="*60)

    set_a = {"python", "javascript", "java", "c++"}
    set_b = {"python", "go", "rust", "java"}

    print(f"\n集合 A: {set_a}")
    print(f"集合 B: {set_b}")

    print(f"\n🔹 聯集 (A | B): {set_a | set_b}")
    print(f"   所有語言")

    print(f"\n🔹 交集 (A & B): {set_a & set_b}")
    print(f"   共同語言")

    print(f"\n🔹 差集 (A - B): {set_a - set_b}")
    print(f"   只在 A 中的語言")

    print(f"\n🔹 差集 (B - A): {set_b - set_a}")
    print(f"   只在 B 中的語言")

    print(f"\n🔹 對稱差集 (A ^ B): {set_a ^ set_b}")
    print(f"   不重複的語言")

    print(f"\n🔹 子集檢查:")
    print(f"   {{'python', 'java'}} <= A: {{'python', 'java'} <= set_a}")

    print(f"\n🔹 超集檢查:")
    print(f"   A >= {{'python'}}: {set_a >= {'python'}}")


def main():
    manager = TagManager()

    print("""
╔══════════════════════════════════════════════════════╗
║            標籤管理系統 v1.0                           ║
║           展示 Python 集合的應用                       ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print(f"""
🏷️  標籤管理 | 文章: {len(manager.articles)} | 標籤: {len(manager.all_tags)}

【選單】
  1. 查看所有文章      2. 新增文章
  3. 依標籤搜尋        4. 標籤統計
  5. 相似度分析        6. 集合運算展示
  7. 載入範例資料      0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            display_articles(manager.articles)

        elif choice == '2':
            title = input("文章標題: ").strip()
            if not title:
                print("❌ 標題不能為空！")
                continue

            tags_input = input("標籤 (逗號分隔): ").strip()
            tags = [t.strip() for t in tags_input.split(',') if t.strip()]

            article = manager.add_article(title, tags)
            print(f"✅ 已新增: {article.title}")
            print(f"   標籤: {', '.join(f'#{t}' for t in article.tags)}")

        elif choice == '3':
            if not manager.articles:
                print("❌ 尚無文章！")
                continue

            print(f"\n可用標籤: {', '.join(sorted(manager.all_tags))}")
            print("\n搜尋模式: 1.任一符合 2.全部符合")
            mode = input("選擇: ").strip()

            tags_input = input("輸入標籤 (逗號分隔): ").strip()
            tags = [t.strip() for t in tags_input.split(',') if t.strip()]

            if mode == '2':
                results = manager.get_articles_by_all_tags(tags)
                display_articles(results, f"包含所有標籤: {', '.join(tags)}")
            else:
                results = manager.get_articles_by_any_tags(tags)
                display_articles(results, f"包含任一標籤: {', '.join(tags)}")

        elif choice == '4':
            stats = manager.get_tag_statistics()
            print("\n📊 標籤使用統計")
            print("=" * 40)

            if not stats:
                print("  (尚無標籤)")
            else:
                max_count = max(stats.values())
                for tag, count in stats.items():
                    bar = "█" * int(count / max_count * 20)
                    print(f"  #{tag:15} {bar} ({count})")

        elif choice == '5':
            if len(manager.articles) < 2:
                print("❌ 需要至少 2 篇文章！")
                continue

            display_articles(manager.articles)
            try:
                idx = int(input("選擇一篇文章 (編號): ")) - 1
                if 0 <= idx < len(manager.articles):
                    article = manager.articles[idx]
                    similar = manager.find_similar_articles(article, 0.2)

                    print(f"\n🔍 與「{article.title}」相似的文章:")
                    print("=" * 50)

                    if not similar:
                        print("  找不到相似文章")
                    else:
                        for other, sim in similar:
                            common = manager.get_common_tags(article, other)
                            print(f"\n  📄 {other.title}")
                            print(f"     相似度: {sim:.1%}")
                            print(f"     共同標籤: {', '.join(f'#{t}' for t in common)}")

                else:
                    print("❌ 無效的編號！")
            except ValueError:
                print("❌ 請輸入數字！")

        elif choice == '6':
            demonstrate_set_operations()

        elif choice == '7':
            manager.add_sample_data()
            print("✅ 已載入範例資料！")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
