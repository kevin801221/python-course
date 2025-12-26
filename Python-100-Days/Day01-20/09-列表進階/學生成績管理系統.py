"""
學生成績管理系統 - Student Grade Manager
========================================
進階應用：展示 Python 列表進階操作

功能：
1. 多維列表管理
2. 列表切片操作
3. 排序與統計
4. 資料分析
"""

import random
from datetime import datetime


class GradeManager:
    """成績管理器"""

    SUBJECTS = ["國文", "英文", "數學", "自然", "社會"]

    def __init__(self):
        # 二維列表: [[學生資料], [學生資料], ...]
        # 學生資料: [姓名, 國文, 英文, 數學, 自然, 社會]
        self.students = []

    def add_student(self, name, scores=None):
        """新增學生"""
        if scores is None:
            scores = [0] * len(self.SUBJECTS)
        # 使用列表連接
        student = [name] + scores
        self.students.append(student)
        return student

    def get_student(self, index):
        """取得學生 - 索引存取"""
        if 0 <= index < len(self.students):
            return self.students[index]
        return None

    def update_score(self, student_idx, subject_idx, score):
        """更新分數 - 二維索引"""
        if 0 <= student_idx < len(self.students):
            if 0 <= subject_idx < len(self.SUBJECTS):
                # +1 是因為第一個元素是姓名
                self.students[student_idx][subject_idx + 1] = score
                return True
        return False

    def get_all_scores(self, student_idx):
        """取得某學生所有分數 - 切片"""
        if 0 <= student_idx < len(self.students):
            return self.students[student_idx][1:]  # 排除姓名
        return []

    def get_subject_scores(self, subject_idx):
        """取得某科目所有分數 - 列表推導式"""
        return [s[subject_idx + 1] for s in self.students]

    def calculate_average(self, scores):
        """計算平均 - 使用 sum() 和 len()"""
        if not scores:
            return 0
        return sum(scores) / len(scores)

    def get_student_average(self, student_idx):
        """學生平均分"""
        scores = self.get_all_scores(student_idx)
        return self.calculate_average(scores)

    def get_subject_average(self, subject_idx):
        """科目平均分"""
        scores = self.get_subject_scores(subject_idx)
        return self.calculate_average(scores)

    def get_top_students(self, n=5):
        """取得前N名 - 排序與切片"""
        # 建立 (索引, 平均分) 的列表
        averages = [(i, self.get_student_average(i)) for i in range(len(self.students))]
        # 按平均分排序
        averages.sort(key=lambda x: x[1], reverse=True)
        # 取前N名
        return averages[:n]

    def get_rank(self, student_idx):
        """取得排名"""
        averages = [(i, self.get_student_average(i)) for i in range(len(self.students))]
        averages.sort(key=lambda x: x[1], reverse=True)
        for rank, (idx, _) in enumerate(averages, 1):
            if idx == student_idx:
                return rank
        return -1

    def get_grade_distribution(self, subject_idx):
        """成績分布"""
        scores = self.get_subject_scores(subject_idx)
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

        for score in scores:
            if score >= 90:
                distribution['A'] += 1
            elif score >= 80:
                distribution['B'] += 1
            elif score >= 70:
                distribution['C'] += 1
            elif score >= 60:
                distribution['D'] += 1
            else:
                distribution['F'] += 1

        return distribution

    def generate_sample_data(self, n=10):
        """產生範例資料"""
        names = ["王小明", "李大華", "張美麗", "陳建國", "林志偉",
                 "黃雅婷", "劉俊傑", "吳淑芬", "蔡宗翰", "楊雅琪",
                 "周志豪", "許雅雯", "鄭宏偉", "謝佳穎", "郭俊賢"]

        random.shuffle(names)
        for name in names[:n]:
            scores = [random.randint(40, 100) for _ in self.SUBJECTS]
            self.add_student(name, scores)


def display_table(manager):
    """顯示成績表格"""
    print("\n" + "=" * 75)
    print(f"{'姓名':^8}", end="")
    for subject in manager.SUBJECTS:
        print(f"{subject:^8}", end="")
    print(f"{'平均':^8}{'排名':^6}")
    print("-" * 75)

    for i, student in enumerate(manager.students):
        name = student[0]
        scores = student[1:]
        avg = manager.get_student_average(i)
        rank = manager.get_rank(i)

        print(f"{name:^8}", end="")
        for score in scores:
            print(f"{score:^8}", end="")
        print(f"{avg:^8.1f}{rank:^6}")

    print("=" * 75)


def display_subject_stats(manager):
    """顯示科目統計"""
    print("\n" + "=" * 60)
    print("                   科目統計分析")
    print("=" * 60)

    for i, subject in enumerate(manager.SUBJECTS):
        scores = manager.get_subject_scores(i)
        avg = manager.get_subject_average(i)
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0
        dist = manager.get_grade_distribution(i)

        print(f"\n【{subject}】")
        print(f"  平均: {avg:.1f} | 最高: {max_score} | 最低: {min_score}")
        print(f"  分布: A:{dist['A']} B:{dist['B']} C:{dist['C']} D:{dist['D']} F:{dist['F']}")

        # 視覺化分布
        total = len(scores)
        if total > 0:
            bar = ""
            for grade in ['A', 'B', 'C', 'D', 'F']:
                width = int(dist[grade] / total * 20)
                bar += "█" * width
            print(f"  圖表: [{bar:20}]")


def main():
    manager = GradeManager()

    print("""
╔══════════════════════════════════════════════════════╗
║            學生成績管理系統 v1.0                       ║
║           展示 Python 列表進階操作                     ║
╚══════════════════════════════════════════════════════╝
    """)

    while True:
        print(f"""
📊 成績管理 | 共 {len(manager.students)} 位學生

【選單】
  1. 查看成績表     2. 新增學生     3. 修改成績
  4. 科目統計       5. 排名榜       6. 載入範例
  0. 退出
""")

        choice = input("請選擇: ").strip()

        if choice == '0':
            print("\n再見！")
            break

        elif choice == '1':
            if manager.students:
                display_table(manager)
            else:
                print("❌ 尚無學生資料！")

        elif choice == '2':
            name = input("學生姓名: ").strip()
            if not name:
                print("❌ 姓名不能為空！")
                continue

            scores = []
            for subject in manager.SUBJECTS:
                while True:
                    try:
                        score = int(input(f"{subject} 成績: "))
                        if 0 <= score <= 100:
                            scores.append(score)
                            break
                        print("分數應在 0-100 之間！")
                    except ValueError:
                        print("請輸入數字！")

            manager.add_student(name, scores)
            print(f"✅ 已新增學生: {name}")

        elif choice == '3':
            if not manager.students:
                print("❌ 尚無學生資料！")
                continue

            display_table(manager)
            try:
                s_idx = int(input("選擇學生編號: ")) - 1
                print(f"科目: {', '.join(f'{i+1}.{s}' for i, s in enumerate(manager.SUBJECTS))}")
                sub_idx = int(input("選擇科目: ")) - 1
                new_score = int(input("新分數: "))

                if manager.update_score(s_idx, sub_idx, new_score):
                    print("✅ 成績已更新！")
                else:
                    print("❌ 無效的選擇！")
            except ValueError:
                print("❌ 請輸入數字！")

        elif choice == '4':
            if manager.students:
                display_subject_stats(manager)
            else:
                print("❌ 尚無學生資料！")

        elif choice == '5':
            if not manager.students:
                print("❌ 尚無學生資料！")
                continue

            print("\n🏆 成績排名榜")
            print("=" * 40)
            top = manager.get_top_students(len(manager.students))

            for rank, (idx, avg) in enumerate(top, 1):
                name = manager.students[idx][0]
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
                print(f"  {medal} 第{rank:2}名: {name:8} 平均: {avg:.1f}")

            print("=" * 40)

        elif choice == '6':
            n = input("產生幾位學生? (預設10): ").strip()
            n = int(n) if n.isdigit() else 10
            manager.generate_sample_data(n)
            print(f"✅ 已產生 {n} 位學生的範例資料！")

        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    main()
