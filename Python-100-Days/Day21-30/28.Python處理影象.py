#!/usr/bin/env python3
"""
從 28.Python处理图像.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
from PIL import Image
   
   # 讀取影象獲得Image物件
   image = Image.open('guido.jpg')
   # 透過Image物件的format屬性獲得影象的格式
   print(image.format) # JPEG
   # 透過Image物件的size屬性獲得影象的尺寸
   print(image.size)   # (500, 750)
   # 透過Image物件的mode屬性獲取影象的模式
   print(image.mode)   # RGB
   # 透過Image物件的show方法顯示影象
   image.show()
# === 範例 2 ===
# 透過Image物件的crop方法指定剪裁區域剪裁影象
   image.crop((80, 20, 310, 360)).show()
# === 範例 3 ===
# 透過Image物件的thumbnail方法生成指定尺寸的縮圖
   image.thumbnail((128, 128))
   image.show()
# === 範例 4 ===
# 讀取Kevin的照片獲得Image物件
   luohao_image = Image.open('luohao.png')
   # 讀取吉多的照片獲得Image物件
   guido_image = Image.open('guido.jpg')
   # 從吉多的照片上剪裁出吉多的頭
   guido_head = guido_image.crop((80, 20, 310, 360))
   width, height = guido_head.size
   # 使用Image物件的resize方法修改影象的尺寸
   # 使用Image物件的paste方法將吉多的頭貼上到Kevin的照片上
   luohao_image.paste(guido_head.resize((int(width / 1.5), int(height / 1.5))), (172, 40))
   luohao_image.show()
# === 範例 5 ===
image = Image.open('guido.jpg')
   # 使用Image物件的rotate方法實現影象的旋轉
   image.rotate(45).show()
   # 使用Image物件的transpose方法實現影象翻轉
   # Image.FLIP_LEFT_RIGHT - 水平翻轉
   # Image.FLIP_TOP_BOTTOM - 垂直翻轉
   image.transpose(Image.FLIP_TOP_BOTTOM).show()
# === 範例 6 ===
for x in range(80, 310):
       for y in range(20, 360):
           # 透過Image物件的putpixel方法修改影象指定畫素點
           image.putpixel((x, y), (128, 128, 128))
   image.show()
# === 範例 7 ===
from PIL import ImageFilter
   
   # 使用Image物件的filter方法對影象進行濾鏡處理
   # ImageFilter模組包含了諸多預設的濾鏡也可以自定義濾鏡
   image.filter(ImageFilter.CONTOUR).show()
# === 範例 8 ===
import random

from PIL import Image, ImageDraw, ImageFont


def random_color():
    """生成隨機顏色"""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return red, green, blue


width, height = 800, 600
# 建立一個800*600的影象，背景色為白色
image = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
# 建立一個ImageDraw物件
drawer = ImageDraw.Draw(image)
# 透過指定字型和大小獲得ImageFont物件
font = ImageFont.truetype('Kongxin.ttf', 32)
# 透過ImageDraw物件的text方法繪製文字
drawer.text((300, 50), 'Hello, world!', fill=(255, 0, 0), font=font)
# 透過ImageDraw物件的line方法繪製兩條對角直線
drawer.line((0, 0, width, height), fill=(0, 0, 255), width=2)
drawer.line((width, 0, 0, height), fill=(0, 0, 255), width=2)
xy = width // 2 - 60, height // 2 - 60, width // 2 + 60, height // 2 + 60
# 透過ImageDraw物件的rectangle方法繪製矩形
drawer.rectangle(xy, outline=(255, 0, 0), width=2)
# 透過ImageDraw物件的ellipse方法繪製橢圓
for i in range(4):
    left, top, right, bottom = 150 + i * 120, 220, 310 + i * 120, 380
    drawer.ellipse((left, top, right, bottom), outline=random_color(), width=8)
# 顯示影象
image.show()
# 儲存影象
image.save('result.png')
