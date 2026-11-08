# -*- coding: utf-8 -*-
"""准备站点所需图片资源：LOGO / ICO / 二维码裁切"""
import os
import shutil
from PIL import Image

ROOT = r"D:\项目管理文件夹\2026-11-08-11-48-17"
SRC_LOGO = r"D:\项目管理\logo设计\logos\export-20260930\icon-512-transparent.png"
SRC_ICON = r"D:\项目管理\logo设计\logos\export-20260930\icon-192.png"
SRC_QR = r"C:\Users\SAMSUNG\Documents\xwechat_files\piweih_eab9\temp\RWTemp\2026-11\702673143d4fb07dd9d916e429687a37.png"
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)

# 1. 站点 LOGO（透明底，等比缩到 256）
logo = Image.open(SRC_LOGO).convert("RGBA")
logo.thumbnail((256, 256), Image.LANCZOS)
logo.save(os.path.join(OUT, "logo.png"))
print("logo.png", logo.size)

# 2. icon-192 原图另存 + 生成多尺寸 favicon.ico
icon = Image.open(SRC_ICON).convert("RGBA")
shutil.copyfile(SRC_ICON, os.path.join(OUT, "icon-192.png"))
icon.save(os.path.join(ROOT, "favicon.ico"),
          format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("favicon.ico / icon-192.png", icon.size)

# 3. 微信二维码：按蓝色像素定位并裁切，去掉头像与姓名区域
qr = Image.open(SRC_QR).convert("RGB")
w, h = qr.size
px = qr.load()
minx, miny, maxx, maxy = w, h, 0, 0
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        if b > 135 and (b - r) > 45 and (b - g) > 18:
            if x < minx: minx = x
            if y < miny: miny = y
            if x > maxx: maxx = x
            if y > maxy: maxy = y
print("qr blue bbox", (minx, miny, maxx, maxy), "source", (w, h))
pad = 26
box = (max(0, minx - pad), max(0, miny - pad), min(w, maxx + pad), min(h, maxy + pad))
crop = qr.crop(box)
crop.save(os.path.join(OUT, "qrcode.png"))
print("qrcode.png", crop.size, box)

# 4. 原图留档
shutil.copyfile(SRC_QR, os.path.join(OUT, "qrcode-source.png"))
