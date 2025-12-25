#!/usr/bin/env python3
"""
從 80.数据可视化-3.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from pyecharts.globals import CurrentConfig, NotebookType

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB
# === 範例 2 ===
bar_chart.render_notebook()
# === 範例 3 ===
pie_chart.render_notebook()
# === 範例 4 ===
map_chart.render_notebook()
