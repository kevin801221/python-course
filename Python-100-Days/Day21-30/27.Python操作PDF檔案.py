#!/usr/bin/env python3
"""
從 27.Python操作PDF文件.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import PyPDF2

reader = PyPDF2.PdfReader('test.pdf')
for page in reader.pages:
    print(page.extract_text())
# === 範例 2 ===
reader = PyPDF2.PdfReader('XGBoost.pdf')
writer = PyPDF2.PdfWriter()

for no, page in enumerate(reader.pages):
    if no % 2 == 0:
        new_page = page.rotate(-90)
    else:
        new_page = page.rotate(90)
    writer.add_page(new_page)

with open('temp.pdf', 'wb') as file_obj:
    writer.write(file_obj)
# === 範例 3 ===
import PyPDF2

reader = PyPDF2.PdfReader('XGBoost.pdf')
writer = PyPDF2.PdfWriter()

for page in reader.pages:
    writer.add_page(page)
    
writer.encrypt('foobared')

with open('temp.pdf', 'wb') as file_obj:
    writer.write(file_obj)
# === 範例 4 ===
reader1 = PyPDF2.PdfReader('XGBoost.pdf')
reader2 = PyPDF2.PdfReader('watermark.pdf')
writer = PyPDF2.PdfWriter()
watermark_page = reader2.pages[0]

for page in reader1.pages:
    page.merge_page(watermark_page)
    writer.add_page(page)

with open('temp.pdf', 'wb') as file_obj:
    writer.write(file_obj)
# === 範例 5 ===
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdf_canvas = canvas.Canvas('resources/demo.pdf', pagesize=A4)
width, height = A4

# 繪圖
image = canvas.ImageReader('resources/guido.jpg')
pdf_canvas.drawImage(image, 20, height - 395, 250, 375)

# 顯示當前頁
pdf_canvas.showPage()

# 註冊字型檔案
pdfmetrics.registerFont(TTFont('Font1', 'resources/fonts/Vera.ttf'))
pdfmetrics.registerFont(TTFont('Font2', 'resources/fonts/青呱石頭體.ttf'))

# 寫字
pdf_canvas.setFont('Font2', 40)
pdf_canvas.setFillColorRGB(0.9, 0.5, 0.3, 1)
pdf_canvas.drawString(width // 2 - 120, height // 2, '你好，世界！')
pdf_canvas.setFont('Font1', 40)
pdf_canvas.setFillColorRGB(0, 1, 0, 0.5)
pdf_canvas.rotate(18)
pdf_canvas.drawString(250, 250, 'hello, world!')

# 儲存
pdf_canvas.save()
