#!/usr/bin/env python3
"""
從 24.Python读写Excel文件-1.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import xlrd

# 使用xlrd模組的open_workbook函式開啟指定Excel檔案並獲得Book物件（工作簿）
wb = xlrd.open_workbook('阿里巴巴2020年股票資料.xls')
# 透過Book物件的sheet_names方法可以獲取所有表單名稱
sheetnames = wb.sheet_names()
print(sheetnames)
# 透過指定的表單名稱獲取Sheet物件（工作表）
sheet = wb.sheet_by_name(sheetnames[0])
# 透過Sheet物件的nrows和ncols屬性獲取表單的行數和列數
print(sheet.nrows, sheet.ncols)
for row in range(sheet.nrows):
    for col in range(sheet.ncols):
        # 透過Sheet物件的cell方法獲取指定Cell物件（單元格）
        # 透過Cell物件的value屬性獲取單元格中的值
        value = sheet.cell(row, col).value
        # 對除首行外的其他行進行資料格式化處理
        if row > 0:
            # 第1列的xldate型別先轉成元組再格式化為“年月日”的格式
            if col == 0:
                # xldate_as_tuple函式的第二個引數只有0和1兩個取值
                # 其中0代表以1900-01-01為基準的日期，1代表以1904-01-01為基準的日期
                value = xlrd.xldate_as_tuple(value, 0)
                value = f'{value[0]}年{value[1]:>02d}月{value[2]:>02d}日'
            # 其他列的number型別處理成小數點後保留兩位有效數字的浮點數
            else:
                value = f'{value:.2f}'
        print(value, end='\t')
    print()
# 獲取最後一個單元格的資料型別
# 0 - 空值，1 - 字串，2 - 數字，3 - 日期，4 - 布林，5 - 錯誤
last_cell_type = sheet.cell_type(sheet.nrows - 1, sheet.ncols - 1)
print(last_cell_type)
# 獲取第一行的值（列表）
print(sheet.row_values(0))
# 獲取指定行指定列範圍的資料（列表）
# 第一個引數代表行索引，第二個和第三個引數代表列的開始（含）和結束（不含）索引
print(sheet.row_slice(3, 0, 5))
# === 範例 2 ===
import random

import xlwt

student_names = ['關羽', '張飛', '趙雲', '馬超', '黃忠']
scores = [[random.randrange(50, 101) for _ in range(3)] for _ in range(5)]
# 建立工作簿物件（Workbook）
wb = xlwt.Workbook()
# 建立工作表物件（Worksheet）
sheet = wb.add_sheet('一年級二班')
# 新增表頭資料
titles = ('姓名', '語文', '數學', '英語')
for index, title in enumerate(titles):
    sheet.write(0, index, title)
# 將學生姓名和考試成績寫入單元格
for row in range(len(scores)):
    sheet.write(row + 1, 0, student_names[row])
    for col in range(len(scores[row])):
        sheet.write(row + 1, col + 1, scores[row][col])
# 儲存Excel工作簿
wb.save('考試成績表.xls')
# === 範例 3 ===
header_style = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
# 0 - 黑色、1 - 白色、2 - 紅色、3 - 綠色、4 - 藍色、5 - 黃色、6 - 粉色、7 - 青色
pattern.pattern_fore_colour = 5
header_style.pattern = pattern
titles = ('姓名', '語文', '數學', '英語')
for index, title in enumerate(titles):
    sheet.write(0, index, title, header_style)
# === 範例 4 ===
font = xlwt.Font()
# 字型名稱
font.name = '華文楷體'
# 字型大小（20是基準單位，18表示18px）
font.height = 20 * 18
# 是否使用粗體
font.bold = True
# 是否使用斜體
font.italic = False
# 字型顏色
font.colour_index = 1
header_style.font = font
# === 範例 5 ===
align = xlwt.Alignment()
# 垂直方向的對齊方式
align.vert = xlwt.Alignment.VERT_CENTER
# 水平方向的對齊方式
align.horz = xlwt.Alignment.HORZ_CENTER
header_style.alignment = align
# === 範例 6 ===
borders = xlwt.Borders()
props = (
    ('top', 'top_colour'), ('right', 'right_colour'),
    ('bottom', 'bottom_colour'), ('left', 'left_colour')
)
# 透過迴圈對四個方向的邊框樣式及顏色進行設定
for position, color in props:
    # 使用setattr內建函式動態給物件指定的屬性賦值
    setattr(borders, position, xlwt.Borders.DASHED)
    setattr(borders, color, 5)
header_style.borders = borders
# === 範例 7 ===
# 設定行高為40px
sheet.row(0).set_style(xlwt.easyxf(f'font:height {20 * 40}'))
titles = ('姓名', '語文', '數學', '英語')
for index, title in enumerate(titles):
    # 設定列寬為200px
    sheet.col(index).width = 20 * 200
    # 設定單元格的資料和樣式
    sheet.write(0, index, title, header_style)
# === 範例 8 ===
import xlrd
import xlwt
from xlutils.copy import copy

wb_for_read = xlrd.open_workbook('阿里巴巴2020年股票資料.xls')
sheet1 = wb_for_read.sheet_by_index(0)
nrows, ncols = sheet1.nrows, sheet1.ncols
wb_for_write = copy(wb_for_read)
sheet2 = wb_for_write.get_sheet(0)
sheet2.write(nrows, 4, xlwt.Formula(f'average(E2:E{nrows})'))
sheet2.write(nrows, 6, xlwt.Formula(f'sum(G2:G{nrows})'))
wb_for_write.save('阿里巴巴2020年股票資料彙總.xls')
